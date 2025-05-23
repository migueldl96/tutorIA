from io import StringIO
import logging
import tempfile
from typing import Dict, DefaultDict, List
from typing_extensions import TypedDict
from collections import defaultdict
import pandas as pd
from pyBKT.models import Model, Roster
import os
import yaml
import pickle
import dotenv
from repositories.base_repository import BaseRepository

dotenv.load_dotenv()

# Si no se declara, el prior será 0 si estamos en multiprior
# Si se declara aprende un prior general, y otro específico
a_priori_probs = {}

SEED = 42

class DataEntry(TypedDict):
    order_id: int
    user_id: str
    skill_name: str
    correct: int
    item_id: str
    subject_id: str

class StudentResult(TypedDict):
    maestry_prob: float
    correct_prob: float
    maestry_state: str
    
class StudentStates(TypedDict):
    learns: Dict[str, Dict[str, float]]
    forgets: Dict[str, Dict[str, float]]

class SkillStates(TypedDict):
    prior: float
    learns: float
    guesses: float
    slips: float
    forgets: float


class EvaluationResponse(TypedDict):
    status: str
    message: str
    roster_paths: Dict[str, str]


class StudentModel:
    """
    This is a placeholder class for the model that evaluates the student.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self.csv_path = os.getenv("CSV_PATH", "datasets/students.csv")
        self.model_path = os.getenv("MODEL_PATH", "models/student_model.pkl")
        self.evaluation_csv_path_non_trained = os.getenv(
            "EVALUATION_CSV_PATH_NON_TRAINED", "datasets/evaluation_non_trained.csv"
        )
        self.evaluation_csv_path_trained = os.getenv(
            "EVALUATION_CSV_PATH_TRAINED", "datasets/evaluation_trained.csv"
        )
        self.evaluation_path = os.getenv(
            "EVALUATION_PATH", "datasets/evaluation"
        )
        self.student_model = None
        self.roster = None
        

    def start_real_time_evaluation(
        self, user_id: str, skill_names: List[str]
    ) -> EvaluationResponse:
        """
        Inicia la evaluación en tiempo real para un estudiante y unas habilidades.
        Crea un nuevo roster para el estudiante y guarda la configuración en un archivo YAML.
        En caso de existir, devuelve su ruta.

        Args:
            user_id (str): ID del estudiante.
            skill_names (list[str]): Lista de nombres de habilidades.
        Returns:
            EvaluationResponse: Diccionario con el estado de la evaluación:
                - status (str): 'ok' o 'error'.
                - message (str): Mensaje explicativo.
                - roster_paths (Dict[str, str]): Mapeo de cada habilidad a su archivo de roster.
        """
        # Plantilla de respuesta
        response: EvaluationResponse = {"status": "", "message": "", "roster_paths": {}}

        logger = logging.getLogger("uvicorn.error")
        logger.info("Starting real time evaluation...")

        # Path al archivo de configuración
        roster_config_path = self.evaluation_path + "/roster_config.yaml"

        # If file exists in repo, download it
        if self.repository.file_exists(roster_config_path):
            roster_config = self.repository.get_file(roster_config_path)
            logger.info(f"Configuration file {roster_config_path} downloaded")
        else:
            roster_config = {}

        user_entry = roster_config.setdefault(user_id, {})
        existing_skills_map = user_entry.setdefault("skills", {})
        # existing_skills_map: { roster_path1: [skillA,skillB], roster_path2: [skillC], ... }

        # Reusar modelos existentes skill a skill
        used_paths = {}
        for path, skills_in_roster in existing_skills_map.items():
            for sk in skill_names:
                if sk in skills_in_roster:
                    used_paths[sk] = path

        # Determinar qué skills aún no tienen roster
        missing = [sk for sk in skill_names if sk not in used_paths]

        # Si hay skills faltantes, crear un nuevo roster sólo para ellas
        if missing:
            # cargar modelo BKT
            if not self.repository.file_exists(self.model_path):
                response.update(status="error", message="Model path does not exist")
                return response
            # cargar el modelo
            model_data = self.repository.get_file(self.model_path)
            student_model = pickle.loads(model_data)
            
            model_params = student_model.params().reset_index()
            a_prioris = model_params.loc[(model_params["param"] == "learns") & (model_params["class"] == user_id)]
            # crear roster para las 'missing'
            roster = Roster(
                students=[user_id],  # o tu lista de usuarios
                skills=missing,
                model=student_model,
            )
            for skill in missing:
                if skill in a_prioris["skill"].values:
                    roster.skill_rosters[skill].students[user_id].current_state['state_prediction']   = a_prioris.loc[a_prioris["skill"] == skill, "value"].values[0]

            # definir ruta donde guardarlo
            skills_str = "_".join(missing)
            roster_fname = f"roster_{user_id}_{skills_str}.pkl"
            roster_path = os.path.join(self.evaluation_path, roster_fname)

            # persistir roster
            self.repository.save_file(roster_path, pickle.dumps(roster))

            # actualizar configuración: asociar cada skill faltante a este mismo archivo
            existing_skills_map[roster_path] = missing
            for sk in missing:
                used_paths[sk] = roster_path

        # Guardar de nuevo la configuración si hemos creado algo
        if missing:
            self.repository.save_file(
                roster_config_path,
                yaml.dump(roster_config).encode("utf-8")
            )

        # 6) Preparar la respuesta
        response["status"] = "ok"
        response["message"] = "Rosters creados/reutilizados por skill"
        response["roster_paths"] = used_paths
        return response

    def real_time_evaluation(
        self,
        order_id: int,
        user_id: str,
        skill_name: str,
        correct: int,
        item_id: str,
        subject_id: str,
        roster_path: str,
    ) -> StudentResult:
        """
        Evalua el estado del estudiante en tiempo real para una sesión de aprendizaje
        en una habilidad específica. Actualiza el estado del estudiante en el roster
        y guarda los resultados en un CSV.

        Args:
            order_id (int): Descripción del índice de orden único de cada pregunta (item_id) respondida por un estudiante. No se puede repetir entre datasets. Ej: numerical_item_id + timestamp.
            user_id (str): ID del estudiante.
            skill_name (str): Nombre de la habilidad.
            correct (int): 1 si la respuesta es correcta, 0 si es incorrecta, -1 si no se ha respondido.
            item_id (str): ID de la pregunta. Se puede repetir indicando que se ha hecho varias veces la misma pregunta.
            subject_id (str): ID de la asignatura. Se puede repetir indicando que se ha hecho varias veces la misma pregunta.
            roster_path (str): Ruta al archivo del roster.
        Raises:
            FileNotFoundError: Si el archivo del roster no se encuentra.
        Returns:
            result (dict[str, str]): Diccionario con el estado del estudiante y la probabilidad de respuesta correcta.
                - state: Estado del estudiante.
                - correct_prob: Probabilidad de respuesta correcta.
                - state_prob: Probabilidad del estado.
        """
        logger = logging.getLogger("uvicorn.error")
        logger.info("Evaluating student data...")
        # Leemos los roster guardados
        # Guardar los roster y skills en un yaml con la ruta al roster
        result = {"state": None, "correct_prob": None, "state_prob": None}

        # Comprobar que el archivo existe
        if not self.repository.file_exists(roster_path):
            logger.error(f"Roster file {roster_path} not found")
            return {"state": None, "correct_prob": None, "state_prob": None}
        # Cargar el roster
        roster_data = self.repository.get_file(roster_path)
        # Deserializar el objeto
        try:
            self.roster = pickle.loads(roster_data)
        except Exception as e:
            logger.error(f"Error loading roster: {e}")
            return {"state": None, "correct_prob": None, "state_prob": None}


        logger.info("Roster loaded successfully")
        logger.info(f"Evaluating student {user_id} in skill {skill_name}")

        # Actualizar roaster
        self.roster.update_state(skill_name, user_id, correct)
        # Evaluar el estado del estudiante
        state = self.roster.get_state(skill_name, user_id)

        # Extraer los datos del estado
        correct_prob = state.current_state["correct_prediction"]
        state_prob = state.current_state["state_prediction"]
        current_state = state.state_type.name
        result["state"] = current_state
        result["correct_prob"] = correct_prob
        result["state_prob"] = state_prob
        logger.info(
            f"Student {user_id} in skill {skill_name} evaluated. Storing data..."
        )
        # Guardamos el roster
        self.repository.save_file(
            roster_path,
            pickle.dumps(self.roster),
        )
        logger.info("Roster updated successfully")

        # Guardar los datos en el CSV
        if not self.repository.file_exists(self.evaluation_csv_path_non_trained):
            # Crear el CSV
            df = {
                "order_id": [order_id],
                "user_id": [user_id],
                "skill_name": [skill_name],
                "correct": [correct],
                "item_id": [item_id],
                "subject_id": [subject_id],
            }
            # Guardar el CSV
            df = pd.DataFrame(df)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            self.repository.save_file(
                self.evaluation_csv_path_non_trained,
                csv_buffer.getvalue(),
            )
            logger.info("Data stored successfully")
        else:
            # Cargar el CSV
            csv_data = self.repository.get_file(self.evaluation_csv_path_non_trained)
            df = pd.read_csv(StringIO(csv_data.decode()))
            new_df = {
                "order_id": [order_id],
                "user_id": [user_id],
                "skill_name": [skill_name],
                "correct": [correct],
                "item_id": [item_id],
                "subject_id": [subject_id],
            }
            new_df = pd.DataFrame(new_df)
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                logger.error(
                    "Column names do not match. It is not possible to update the dataset"
                )
            df = pd.concat([df, new_df], ignore_index=True)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            self.repository.save_file(
                self.evaluation_csv_path_non_trained,
                csv_buffer.getvalue(),
            )
            logger.info("Data stored successfully")
        return result

    def update_dataset_evaluation(
        self,
        del_roaster: bool = False,
    ):
        """Usando los datos de evaluaciones, actualiza el dataset (de existir) y entrena el modelo.

        Args:


        Returns:
            dict: Diccionario con los estados de los estudiantes y habilidades.
                - students_states: DataFrame con los estados de los estudiantes.
                - skills_states: DataFrame con los estados de las habilidades.
        """

        if self.repository.file_exists(self.csv_path):
            # Cargar el CSV
            csv_data = self.repository.get_file(self.csv_path)
            df = pd.read_csv(StringIO(csv_data.decode()))
            if self.repository.file_exists(self.evaluation_csv_path_non_trained):
                # Cargar el CSV de evaluación
                csv_data = self.repository.get_file(
                    self.evaluation_csv_path_non_trained
                )
                new_df = pd.read_csv(StringIO(csv_data.decode()))
            else:
                logging.error("Evaluation CSV file not found")
                return {"students_states": None, "skills_states": None}
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                logging.error(
                    "Column names do not match. It is not possible to update the dataset"
                )
                return {"students_states": None, "skills_states": None}
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            logging.error("Dataset CSV file not found")
            return {"students_states": None, "skills_states": None}

        # Entrenamos según el caso
        try:
            self.student_model = self.train(df)
        except Exception as e:
            logging.error(f"Error training the model: {e}")
            return {"students_states": None, "skills_states": None}

        # Skill in subject
        skill_subject = {}
        for skill in df["skill_name"].tolist():
            skill_subject[skill] = df[df["skill_name"] == skill]["subject_id"].iloc[0]
        students_states = self.calculate_students_states(skill_subject)

        skills_states = self.calculate_skills_states(skill_subject)

        # TODO
        # Lógica para guardar el CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        self.repository.save_file(self.csv_path, csv_buffer.getvalue())

        # Movemos el csv de evaluacion a la ruta de entrenados
        self.repository.delete_file(
            self.evaluation_csv_path_non_trained
        )
        if self.repository.file_exists(self.evaluation_csv_path_trained):
            # Cargar el CSV
            last_trained_csv = self.repository.get_file(
                self.evaluation_csv_path_trained
            )
            last_trained_csv = pd.read_csv(StringIO(last_trained_csv.decode()))
            last_trained_csv = pd.concat([last_trained_csv, new_df], ignore_index=True)
            # Guardar el CSV
            last_trained_csv_buffer = StringIO()
            last_trained_csv.to_csv(last_trained_csv_buffer, index=False)
            self.repository.save_file(
                self.evaluation_csv_path_trained,
                last_trained_csv_buffer.getvalue(),
            )
        else:
            # Guardar el CSV
            last_trained_csv_buffer = StringIO()
            last_trained_csv.to_csv(new_df, index=False)
            self.repository.save_file(
                self.evaluation_csv_path_trained,
                last_trained_csv_buffer.getvalue(),
            )

        if del_roaster:
            # Eliminar contenido de la carpeta de evaluación
            for filename in os.listdir(self.evaluation_path):
                file_path = os.path.join(self.evaluation_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")

        return {"students_states": students_states, "skills_states": skills_states}

    def update_dataset_tabular(
        self,
        order_id: List[int],
        user_id: List[str],
        skill_name: List[str],
        correct: List[int],
        item_id: List[str],
        subject_id: List[str],
    ):
        # item ID no se usa en este caso, pero puede usarse para ver que
        # preguntas son más o menos difíciles de aprender
        # Puedo introducir la lógica pero habría que entrenar otro modelo para ello
        """Actualiza el dataset (de existir) y entrena el modelo.

        Args:
            order_id (list[str]): Descripción del índice de orden único de cada pregunta (item_id) respondida por un estudiante. No se puede repetir entre datasets. Ej: numerical_item_id + timestamp.
            user_id (list[str]): ID del estudiante.
            skill_name (list[str]): Nombre de la habilidad.
            correct (list[int]): 1 si la respuesta es correcta, 0 si es incorrecta, -1 si no se ha respondido.
            item_id (list[str]): ID de la pregunta. Se puede repetir indicando que se ha hecho varias veces la misma pregunta.

        Returns:
            dict: Diccionario con los estados de los estudiantes y habilidades.
                - students_states: DataFrame con los estados de los estudiantes.
                - skills_states: DataFrame con los estados de las habilidades.
        """
        # Comprobar que todos los argumentos son listas

        if self.repository.file_exists(self.csv_path):
            # Cargar el CSV
            df = pd.read_csv(self.repository.get_file(self.csv_path))
            new_df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id,
                "subject_id": subject_id,
            }
            try:
                new_df = pd.DataFrame(new_df)
            except Exception as e:
                logging.error(f"Error creating DataFrame: {e}")
                return {"students_states": None, "skills_states": None}
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                logging.error(
                    "Column names do not match. It is not possible to update the dataset"
                )
                return {"students_states": None, "skills_states": None}

            df = pd.concat([df, new_df], ignore_index=True)
        else:
            # Crear el CSV
            df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id,
                "subject_id": subject_id,
            }
            # Guardar el CSV
            try:
                df = pd.DataFrame(df)
            except Exception as e:
                logging.error(f"Error creating DataFrame: {e}")
                return {"students_states": None, "skills_states": None}

        # Entrenamos según el caso
        try:
            self.student_model = self.train(df)
        except Exception as e:
            logging.error(f"Error training the model: {e}")
            return {"students_states": None, "skills_states": None}

        # Skill in subject
        skill_subject = {}
        for skill in df["skill_name"].tolist():
            skill_subject[skill] = df[df["skill_name"] == skill]["subject_id"].iloc[0]
        students_states = self.calculate_students_states(skill_subject)

        skills_states = self.calculate_skills_states(skill_subject)

        # TODO
        # Lógica para guardar el CSV
        df.to_csv(self.csv_path, index=False)
        return {"students_states": students_states, "skills_states": skills_states}

    def train(self, df : pd.DataFrame) -> Model:
        """
        Entrena el modelo con los datos del Dataframe.

        Args:
            df (pd.Dataframe): DataFrame con los datos de entrenamiento.
        Returns:
            Model(pyBKT.models.Model): Modelo entrenado.
        """
        student_model = Model(seed=SEED)
        # Entrenar el modelo
        student_model.fit(data=df, multiprior="user_id", forgets=True)

        # Lógica para guardar el modelo
        self.repository.save_file(self.model_path, pickle.dumps(student_model))
        return student_model

    def update_dataset(
        self, data: List[DataEntry]):
        # item ID no se usa en este caso, pero puede usarse para ver que
        # preguntas son más o menos difíciles de aprender
        # Puedo introducir la lógica pero habría que entrenar otro modelo para ello
        """Actualiza el dataset (de existir) y entrena el modelo.

        Args:
            order_id (list[str]): Descripción del índice de orden único de cada pregunta (item_id) respondida por un estudiante. No se puede repetir entre datasets. Ej: numerical_item_id + timestamp.
            user_id (list[str]): ID del estudiante.
            skill_name (list[str]): Nombre de la habilidad.
            correct (list[int]): 1 si la respuesta es correcta, 0 si es incorrecta, -1 si no se ha respondido.
            item_id (list[str]): ID de la pregunta. Se puede repetir indicando que se ha hecho varias veces la misma pregunta.

        Returns:
            dict: Diccionario con los estados de los estudiantes y habilidades.
                - students_states: DataFrame con los estados de los estudiantes.
                - skills_states: DataFrame con los estados de las habilidades.
        """
        # Comprobar que todos los argumentos son listas
        # Transformar la entrada (list[DataEntry]) a un Dict con listas
        order_id = [entry["order_id"] for entry in data]
        user_id = [entry["user_id"] for entry in data]
        skill_name = [entry["skill_name"] for entry in data]
        correct = [entry["correct"] for entry in data]
        item_id = [entry["item_id"] for entry in data]
        subject_id = [entry["subject_id"] for entry in data]

        if self.repository.file_exists(self.csv_path):
            data = self.repository.get_file(self.csv_path)
            # Cargar el CSV
            df = pd.read_csv(StringIO(data.decode()))
            new_df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id,
                "subject_id": subject_id,
            }
            try:
                new_df = pd.DataFrame(new_df)
            except Exception as e:
                logging.error(f"Error creating DataFrame: {e}")
                return {"students_states": None, "skills_states": None}
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                logging.error(
                    "Column names do not match. It is not possible to update the dataset"
                )
                return {"students_states": None, "skills_states": None}

            df = pd.concat([df, new_df], ignore_index=True)
        else:
            # Crear el CSV
            df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id,
                "subject_id": subject_id,
            }
            # Guardar el CSV
            try:
                df = pd.DataFrame(df)
            except Exception as e:
                logging.error(f"Error creating DataFrame: {e}")
                return {"students_states": None, "skills_states": None}

        # Entrenamos según el caso
        try:
            self.student_model = self.train(df)
        except Exception as e:
            logging.error(f"Error training the model: {e}")
            return {"students_states": None, "skills_states": None}

        # Skill in subject
        skill_subject = {}
        for skill in df["skill_name"].tolist():
            skill_subject[skill] = df[df["skill_name"] == skill]["subject_id"].iloc[0]
        students_states = self.calculate_students_states(skill_subject)

        skills_states = self.calculate_skills_states(skill_subject)

        # Save the CSV in the repository
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        self.repository.save_file(self.csv_path, csv_buffer.getvalue())
        return {"students_states": students_states, "skills_states": skills_states}

    def calculate_students_states(
        self,
        skill_subject_map: Dict[str, str]
    ) -> Dict[str, StudentStates]:
        """
        Para cada estudiante, devuelve dos mapas ('learns' y 'forgets'),
        cada uno agrupado por subject_id con sus skills y su valor.

        Parameters
        ----------
        skill_subject_map : Dict[str, str]
            Mapea cada skill_name a su subject_id.

        Returns
        -------
        Dict[str, StudentStates]
            Ejemplo de salida:
            {
                'alice': {
                    'learns': {
                        'MATH': {'fractions': 0.23, 'equations': 0.91},
                        'PHYS': {'optics': 0.42}
                    },
                    'forgets': {
                        'MATH': {'fractions': 0.00, 'equations': 0.12},
                        'PHYS': {'optics': 0.05}
                    }
                },
                'bob': { ... }
            }
        """
        if self.student_model is None:
            raise ValueError("Not trained model")

        # 1) extrae un DataFrame plano de parámetros
        params = self.student_model.params().reset_index()

        # 2) filtra solo learns y forgets, excluyendo el “Default”
        learn_df = params[
            (params.param == "learns") &
            (params["class"].str.lower() != "default")
        ]
        forget_df = params[
            (params.param == "forgets") &
            (params["class"].str.lower() != "default")
        ]

        # 3) prepara la salida tipada
        out: Dict[str, StudentStates] = {}

        # auxiliar para crear dict sujetos→{skill:valor}
        def nested_subject_dict() -> DefaultDict[str, Dict[str, float]]:
            return defaultdict(dict)

        alumnos = sorted(set(learn_df["class"]) | set(forget_df["class"]))

        for alumno in alumnos:
            learns_by_subject = nested_subject_dict()
            forgets_by_subject = nested_subject_dict()

            # rellena learns
            for row in learn_df[learn_df["class"] == alumno].itertuples():
                subj = skill_subject_map.get(row.skill, "UNKNOWN")
                learns_by_subject[subj][row.skill] = row.value

            # rellena forgets
            for row in forget_df[forget_df["class"] == alumno].itertuples():
                subj = skill_subject_map.get(row.skill, "UNKNOWN")
                forgets_by_subject[subj][row.skill] = row.value

            out[alumno] = {
                "learns": dict(learns_by_subject),
                "forgets": dict(forgets_by_subject)
            }

        return out


    def calculate_skills_states(
        self, skill_subject_map: Dict[str, str]
    ) -> Dict[str, Dict[str, SkillStates]]:
        """
        Calcula los estados de las habilidades por asignatura.

        Esta función construye un diccionario anidado que agrupa las habilidades por
        asignatura (`subject_id`) y asocia a cada habilidad sus parámetros estimados
        por el modelo BKT: probabilidad a priori (`prior`), tasa de aprendizaje
        (`learns`), tasa de adivinación (`guesses`), tasa de error (`slips`) y tasa
        de olvido (`forgets`).

        Estructura de salida:
        ---------------------
        {
            'MATH': {
                'fractions': {
                    'prior': 0.23,
                    'learns': 0.91,
                    'guesses': 0.40,
                    'slips': 0.05,
                    'forgets': 0.00
                },
                'equations': {
                    ...
                }
            },
            'PHYS': {
                ...
            }
        }

        Parameters
        ----------
        skill_subject_map : Dict[str, str]
            Diccionario que mapea cada habilidad (`skill_name`) con su correspondiente ID
            de asignatura (`subject_id`).

        Raises
        ------
        ValueError
            Si el modelo no ha sido entrenado (`self.student_model is None`).

        Returns
        -------
        Dict[str, Dict[str, Dict[str, float]]]
            Diccionario con los estados de las habilidades organizados por asignatura.
        """

        if self.student_model is None:
            raise ValueError("Not trained model")

        # parámetros en formato plano
        params = self.student_model.params().reset_index()

        #  valores "default"
        params["class"] = params["class"].str.lower()
        default_df = params[params["class"] == "default"]

        # 4) Pivot (skill × param → value)
        wide = default_df.pivot(index="skill", columns="param", values="value")
        # Asegura presencia de todas las columnas
        for col in ["prior", "learns", "guesses", "slips", "forgets"]:
            if col not in wide.columns:
                wide[col] = float("nan")

        # construir diccionario anidado subject → skill → métricas
        out: Dict[str, Dict[str, SkillStates]] = defaultdict(dict)

        for skill, row in wide.iterrows():
            subj = skill_subject_map.get(skill, "UNKNOWN")

            out[subj][skill] = {
                "prior": float(row["prior"]),
                "learns": float(row["learns"]),
                "guesses": float(row["guesses"]),
                "slips": float(row["slips"]),
                "forgets": float(row["forgets"]),
            }

        return dict(out)  # convierte defaultdict en dict normal
