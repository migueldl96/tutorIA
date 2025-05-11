import logging
from typing import Dict, DefaultDict
from collections import defaultdict
import pandas as pd
from pyBKT.models import Model, Roster
import os

# Si no se declara, el prior será 0 si estamos en multiprior
# Si se declara aprende un prior general, y otro específico
a_priori_probs = {
}
CSV_PATH = "ruta_al_csv.csv"
MODEL_PATH = ""
SEED = 42   
class StudentResult:
    '''
    This is a placeholder class for the result of the evaluation.
    '''
    def __init__(self):
        self.maestry_prob = 0.0
        self.correct_prob = 0.0
        self.maestry_state = False

class StudentModel:
    '''
    This is a placeholder class for the model that evaluates the student.
    '''
    def __init__(self):
        self.csv_path = CSV_PATH
        self.model_path = MODEL_PATH
        self.student_model = None
        self.roster = None
        pass

    def real_time_evaluation(self, user_id, skill_name, is_correct):
        '''
        Evaluacion en real time del estudiante.
        '''
        logger = logging.getLogger('uvicorn.error')
        logger.info("Evaluating student data...")
        
    def update_dataset(self, order_id, user_id, skill_name, correct, item_id, subject_id):
        # item ID no se usa en este caso, pero puede usarse para ver que 
        # preguntas son más o menos difíciles de aprender
        # Puedo introducir la lógica pero habría que entrenar otro modelo para ello
        """ Actualiza el dataset (de existir) y entrena el modelo.

        Args:
            order_id (int): Índice de orden único de cada pregunta (item_id) y estudiante (user_id). No se puede repetir entre datasets. Ej: numerical_user_id + numerical_item_id + timestamp.
            user_id (str): ID del estudiante.
            skill_name (str): Nombre de la habilidad.
            correct (int): 1 si la respuesta es correcta, 0 si es incorrecta, -1 si no se ha respondido.
            item_id (str): ID de la pregunta. Se puede repetir indicando que se ha hecho varias veces la misma pregunta.

        Raises:
            ValueError: Si el modelo no ha sido entrenado o si los nombres de las columnas no coinciden.

        Returns:
            dict: Diccionario con los estados de los estudiantes y habilidades.
                - students_states: DataFrame con los estados de los estudiantes.
                - skills_states: DataFrame con los estados de las habilidades.
        """
     
        if os.path.exists(self.csv_path):
            # Cargar el CSV
            df = pd.read_csv(self.csv_path)
            new_df = {
                    "order_id": order_id,
                    "user_id": user_id,
                    "skill_name": skill_name,
                    "correct": correct,
                    "item_id": item_id,
                    "subject_id": subject_id}
            new_df = pd.DataFrame(new_df)
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                raise ValueError("Column names do not match")
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            # Crear el CSV
            df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id,
                "subject_id": subject_id}
            # Guardar el CSV
            df = pd.DataFrame(df)


        # Entrenamos según el caso        
        self.student_model = self.train(df)
        
        # Skill in subject
        skill_subject = {}
        for skill in df["skill_name"].tolist():
            skill_subject[skill] = df[df["skill_name"] == skill]["subject_id"].iloc[0]
        students_states = self.calculate_students_states(skill_subject)
        
        skills_states = self.calculate_skills_states(skill_subject)
        
        
        # TODO
        # Lógica para guardar el CSV
        df.to_csv(self.csv_path, index=False)
        return {
            "students_states": students_states,
            "skills_states": skills_states
        }
        
    def train(self, df):
        """
        Entrena el modelo con los datos del Dataframe.

        Args:
            df (pd.Dataframe): DataFrame con los datos de entrenamiento.
        Returns:
            Model(pyBKT.models.Model): Modelo entrenado.
        """
        student_model = Model(seed=SEED)
        # Entrenar el modelo
        student_model.fit(data=df,
                          multiprior="user_id",
                          forgets=True
                          )
        
        # TODO
        # Lógica para guardar el modelo
        student_model.save(self.model_path)
        return student_model
    
    from typing import Dict


    def calculate_students_states(
            self,
            skill_subject_map: Dict[str, str]
    ) -> Dict[str, Dict[str, Dict[str, Dict[str, float]]]]:
        """
        Calcula los estados de los estudiantes organizados por asignatura y habilidad.

        Esta función construye un diccionario anidado que contiene, para cada estudiante,
        las tasas de aprendizaje (`learns`) y de olvido (`forgets`) por habilidad,
        agrupadas a su vez por asignatura (`subject_id`).

        Estructura de salida:
        ---------------------
        ::

            {
                'student_id': {
                    'learns': {
                        'subject_id': {
                            'skill_id': value,
                            ...
                        },
                        ...
                    },
                    'forgets': {
                        'subject_id': {
                            'skill_id': value,
                            ...
                        },
                        ...
                    }
                },
                ...
            }

        Parameters
        ----------
        skill_subject_map : Dict[str, str]
            Diccionario que mapea el nombre de cada habilidad (`skill_name`) con su
            correspondiente ID de asignatura (`subject_id`).

        Raises
        ------
        ValueError
            Si el modelo no ha sido entrenado (`self.student_model is None`).

        Returns
        -------
        Dict[str, Dict[str, Dict[str, Dict[str, float]]]]
            Diccionario con los estados de los estudiantes, organizados por estudiante,
            tipo de parámetro (`learns` o `forgets`), asignatura y habilidad.
        """
        if self.student_model is None:
            raise ValueError("Not trained model")

        # parámetros planos
        params = self.student_model.params().reset_index()

        # filtrar learns / forgets, excluyendo 'Default'
        learn_df = params[
            (params.param == 'learns') &
            (params['class'].str.lower() != 'default')
        ]
        forget_df = params[
            (params.param == 'forgets') &
            (params['class'].str.lower() != 'default')
        ]

        # 4) Construcción de la salida
        out: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {}

        alumnos = sorted(set(learn_df['class']).union(forget_df['class']))

        def nested_dict() -> DefaultDict[str, Dict[str, float]]:
            """Devuelve dict anidado subject → {skill: value}."""
            return defaultdict(dict)

        for alumno in alumnos:
            # Diccionarios vacíos con un nivel para subject_id
            learns_by_subject: DefaultDict[str, Dict[str, float]] = nested_dict()
            forgets_by_subject: DefaultDict[str, Dict[str, float]] = nested_dict()

            #  Learns
            for row in learn_df[learn_df['class'] == alumno].itertuples():
                subj = skill_subject_map.get(row.skill, "UNKNOWN")
                learns_by_subject[subj][row.skill] = row.value

            #  Forgets
            for row in forget_df[forget_df['class'] == alumno].itertuples():
                subj = skill_subject_map.get(row.skill, "UNKNOWN")
                forgets_by_subject[subj][row.skill] = row.value

            out[alumno] = {
                'learns':  dict(learns_by_subject),   # casteo a dict normal
                'forgets': dict(forgets_by_subject)
            }

        return out


    def calculate_skills_states(
            self,
            skill_subject_map: Dict[str, str]
    ) -> Dict[str, Dict[str, Dict[str, float]]]:
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
        params['class'] = params['class'].str.lower()
        default_df = params[params['class'] == 'default']

        # 4) Pivot (skill × param → value)
        wide = default_df.pivot(index='skill', columns='param', values='value')
        # Asegura presencia de todas las columnas
        for col in ['prior', 'learns', 'guesses', 'slips', 'forgets']:
            if col not in wide.columns:
                wide[col] = float('nan')

        # construir diccionario anidado subject → skill → métricas
        out: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(dict)

        for skill, row in wide.iterrows():
            subj = skill_subject_map.get(skill, "UNKNOWN")

            out[subj][skill] = {
                'prior'   : float(row['prior']),
                'learns'  : float(row['learns']),
                'guesses' : float(row['guesses']),
                'slips'   : float(row['slips']),
                'forgets' : float(row['forgets'])
            }

        return dict(out)      # convierte defaultdict en dict normal
