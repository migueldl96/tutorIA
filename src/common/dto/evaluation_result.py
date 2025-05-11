from pydantic import BaseModel, Field, StringConstraints, conint
from typing import List, Optional, Annotated
from datetime import datetime

class InitialEvaluationDTO(BaseModel):
    '''
    Evaluacion inicial de un alumno en una asignatura.
    '''
    student_id: Annotated[
        str,
        StringConstraints(min_length=1)
    ] = Field(..., description="Identificador único del alumno")
    
    subject_code: Annotated[
        str,
        StringConstraints(min_length=1)
    ] = Field(..., description="Código de la asignatura evaluada")
    
    evaluation_date: datetime = Field(default_factory=datetime.utcnow, description="Fecha en que se realizó la evaluación")
    
    skillset_name: str = Field(..., description="Nombre del skillset evaluado")

    skillset_score: int = Field(..., description="Puntuación del skillset evaluado, de 0 a 10")
    
    overall_comment: Optional[str] = Field(None, description="Comentario general del alumno sobre la materia o su preparación")
