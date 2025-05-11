import logging
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
        
    def update_dataset(self, order_id, user_id, skill_name, correct, item_id):
        # item ID no se usa en este caso, pero puede usarse para ver que 
        # preguntas son más o menos difíciles de aprender
        # Puedo introducir la lógica pero habría que entrenar otro modelo para ello
        
        '''
        Logica para la primera evaluacion
        
        1. Recibir la ifnormacion
        2. Cargar el CSV (Si existe)
        3. Actualizar CSV
        4. Entrenar modelo completo (no es óptimo, pero partial_fit no funciona bien)
        5. Guardar modelo y CSVexist
        
        6. Devolver estados iniciales de estudiante
        '''
     
        if os.path.exists(self.csv_path):
            # Cargar el CSV
            df = pd.read_csv(self.csv_path)
            new_df = {
                    "order_id": order_id,
                    "user_id": user_id,
                    "skill_name": skill_name,
                    "correct": correct,
                    "item_id": item_id}
            new_df = pd.DataFrame(new_df)
            # Comprobar que coinciden los nombres de las columnas
            if not all(col in df.columns for col in new_df.columns):
                raise ValueError("Column names do not match")
            df = pd.concat([df, new_df], ignore_index=True)
            # TODO
            # Lógica para guardar el CSV
            df.to_csv(self.csv_path, index=False)
        else:
            # Crear el CSV
            df = {
                "order_id": order_id,
                "user_id": user_id,
                "skill_name": skill_name,
                "correct": correct,
                "item_id": item_id}
            # Guardar el CSV
            df = pd.DataFrame(df)
            # TODO
            # Lógica para guardar el CSV
            df.to_csv(self.csv_path, index=False)

        # Entrenamos según el caso        
        self.student_model = self.train(df)
        
        students_states = self.calculate_students_states()
        skills_states = self.calculate_skills_states()
        
        return {
            "students_states": students_states,
            "skills_states": skills_states
        }
        
    def train(self, df):
        '''
        Entrenamiento del modelo
        '''
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
    
    def calculate_students_states(self):
        """
        Calcular los estados de los estudiantes. Devuleve un DataFrame con los estados de los estudiantes.
        El DataFrame tiene las siguientes columnas:
            - user_id: ID del estudiante.
            - skill: Nombre de la habilidad.
            - learns: Probabilidad de aprender la habilidad.
            - forgets: Probabilidad de olvidar la habilidad.

        Raises:
            ValueError: Si el modelo no ha sido entrenado.

        Returns:
            pd.DataFrame: DataFrame con los estados de los estudiantes.
        """
        if self.student_model is None:
            raise ValueError("Not trained model")
        
        params = self.student_model.params().reset_index()  

        # Filtra sólo learns y forgets
        learn_df  = params[params.param == 'learns' ].copy()
        forget_df = params[params.param == 'forgets'].copy()

        # Pivot para que:
        #    index = class (→ user_id), columns = skill, values = value
        learn_pivot  = learn_df.pivot(index='class', columns='skill', values='value')
        forget_pivot = forget_df.pivot(index='class', columns='skill', values='value')

        learn_pivot .index.name = 'user_id'
        forget_pivot.index.name = 'user_id'

        # Columnas para aprender y olvidar
        learn_pivot.columns  = [f"{skill}_learn"  for skill in learn_pivot.columns]
        forget_pivot.columns = [f"{skill}_forget" for skill in forget_pivot.columns]

        # Unimos en un solo dataframe
        results = pd.concat([learn_pivot, forget_pivot], axis=1).reset_index()
        # Eliminar fila con user_id = "Default"
        results = results[results['user_id'] != 'Default']
        return results
    
    def calculate_skills_states(self):
        """
        Calcular los estados de las habilidades. Devuleve un DataFrame con los estados de las habilidades.
        El DataFrame tiene las siguientes columnas:
            - skill: Nombre de la habilidad.
            - prior: Probabilidad a priori de la habilidad.
            - learns: Probabilidad de aprender la habilidad.
            - guesses: Probabilidad de adivinar la habilidad.
            - slips: Probabilidad de cometer errores en la habilidad.
            - forgets: Probabilidad de olvidar la habilidad.
        Raises:
            ValueError: Si el modelo no ha sido entrenado.

        Returns:
            pd.DataFrame: DataFrame con los estados de las habilidades.
        """

        if self.student_model is None:
            raise ValueError("Not trained model")

        params = self.student_model.params().reset_index()
        # Convertimos a minúsculas para evitar problemas de mayúsculas
        params['class'] = params['class'].str.lower()
        default_params = params[params['class'] == 'default']
        results = default_params.pivot(index='skill', columns='param', values='value')
        # Cambiamos el nombre de las columnas para que coincidan
        results = results[['prior', 'learns', 'guesses', 'slips', 'forgets']]
        results = results.reset_index()
        results.columns.name = None
        return results