from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .models import StudentModel
from pydantic import BaseModel

router = APIRouter(prefix="/evaluation")
model = StudentModel()

# Definir modelos de datos para la API
class TrainingData(BaseModel):
    order_id: List[int]
    user_id: List[str]
    skill_name: List[str]
    correct: List[int]
    item_id: List[str]
    subject_id: List[str]

class EvaluationSetup(BaseModel):
    user_id: str
    skill_names: List[str]

@router.post("/update_dataset")
async def update_dataset(data: TrainingData):
    try:
        results = model.update_dataset(
            order_id=data.order_id,
            user_id=data.user_id,
            skill_name=data.skill_name,
            correct=data.correct,
            item_id=data.item_id,
            subject_id=data.subject_id
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start_real_time_evaluation")
async def start_real_time_evaluation(data: EvaluationSetup):
    try:
        results = model.start_real_time_evaluation(
            user_id=data.user_id,
            skill_names=data.skill_names
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))