from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .models import StudentModel, DataEntry
from pydantic import BaseModel

router = APIRouter(prefix="/evaluation")
model = StudentModel()

# Definir modelos de datos para la API
class TrainingDataTabular(BaseModel):
    order_id: List[int]
    user_id: List[str]
    skill_name: List[str]
    correct: List[int]
    item_id: List[str]
    subject_id: List[str]

class TrainingData(BaseModel):
    data: List[DataEntry]

class RealEvalData(BaseModel):
    order_id: int
    user_id: str
    skill_name: str
    correct: int
    item_id: str
    subject_id: str
    roaster_path: str

class UpdateEvalData(BaseModel):
    del_roaster: bool

class EvaluationSetup(BaseModel):
    user_id: str
    skill_names: List[str]

@router.post("/update_dataset")
async def update_dataset(data: TrainingData):
    try:
        results = model.update_dataset(
            data=data.data
        )           
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update_dataset_tabular")
async def update_dataset(data: TrainingDataTabular):
    try:
        results = model.update_dataset_tabular(
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
    
@router.post("/real_time_evaluation")
async def real_time_evaluation(data: RealEvalData):
    try:
        results = model.real_time_evaluation(
            order_id=data.order_id,
            user_id=data.user_id,
            skill_name=data.skill_name,
            correct=data.correct,
            item_id=data.item_id,
            subject_id=data.subject_id,
            roster_path=data.roaster_path
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update_dataset_evaluation")
async def update_dataset_evaluation(data: UpdateEvalData):
    try:
        results = model.update_dataset_evaluation(
            del_roaster=data.del_roaster
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))