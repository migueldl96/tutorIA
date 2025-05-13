import logging

a_priori_probs = {
    "skill_name": 2.0,
}

class Result:
    '''
    This is a placeholder class for the result of the evaluation.
    '''
    def __init__(self, user_id, skillset_name, is_correct):
        self.maestry_prob = 0.0
        self.correct_prob = 0.0
        self.maestry_state = False

class SomeRandomModel:
    '''
    This is a placeholder class for the model that evaluates the student.
    '''
    def __init__(self):
        pass

    def real_time_evaluation(self, user_id, skillset_name, is_correct):
        '''
        Evaluacion en real time del estudiante.
        '''
        logger = logging.getLogger('uvicorn.error')
        logger.info("Evaluating student data...")
        
    def update_dataset(self, user_id, skillset_name, is_correct):
        '''
        Logica para la primera evaluacion
        
        1. Recibir la ifnormacion
        2. Cargar el CSV (Si existe)
         2.1 Si existe, hace run aprtial fit
         2.2 Si no existe, hace run fit
        3. Actualizar CSV
        4. Guardar modelo y CSV
        
        5. Devolver estados iniciales de estudiante
        '''
        pass
