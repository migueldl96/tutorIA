from pydantic import BaseModel, Field, StringConstraints, conint
from typing import List, Optional, Annotated
from datetime import datetime


class AspectEvaluation(BaseModel):
    '''
    Aspecto a evaluar entre 0 y 10 dentro de una asignatura.
    Ejemplo: La asignatura 'Física' puede tener los siguientes aspectos a evaluar:
        - Matemáticas
        - Algebra
        - Química

    '''
    aspect_name: Annotated[
        str,
        StringConstraints(min_length=1)
    ] = Field(..., description="Nombre del aspecto evaluado, por ejemplo: 'Conocimientos previos', 'Motivación', etc.")
    
    score: Annotated[
        int,
        conint(ge=0, le=10)
    ] = Field(..., description="Puntuación del aspecto evaluado, de 0 a 10")
    
    comments: Optional[str] = Field(None, description="Comentarios adicionales del alumno sobre este aspecto")


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
    
    aspects: List[AspectEvaluation] = Field(..., description="Lista de puntuaciones parciales por aspecto")
    
    overall_comment: Optional[str] = Field(None, description="Comentario general del alumno sobre la materia o su preparación")
