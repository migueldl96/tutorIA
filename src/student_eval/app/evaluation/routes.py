from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .models import StudentModel, DataEntry
from pydantic import BaseModel
from fastapi import Request  # Importar Request
from repositories import AzureBlobRepository
router = APIRouter(prefix="/evaluation")

# Init backend repository
blob_repo = AzureBlobRepository("tutoria")

# Inicializar el modelo
model = StudentModel(blob_repo)

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

class DeleteRoasterData(BaseModel):
    user_id: str
    
@router.post("/update_dataset")
async def update_dataset(request: Request):
    try:
        # Obtener los datos JSON directamente
        data = await request.json()
        
        # Imprimir los datos recibidos para depuración
        print("Datos recibidos:", data)
        
        # Verificar si es una lista o un objeto
        if isinstance(data, list):
            results = model.update_dataset(data=data)
        elif isinstance(data, dict) and "data" in data:
            results = model.update_dataset(data=data["data"])
        else:
            raise HTTPException(status_code=400, detail="Se esperaba una lista de objetos o un objeto con campo 'data'")
        return results
    except Exception as e:
        # SI la excepción es ValueError, devolver un error 400
        if isinstance(e, ValueError):
            raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
        # Para otras excepciones, devolver un error 500
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.post("/update_dataset_tabular")
async def update_dataset_tabular(data: TrainingDataTabular):
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
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update_dataset_evaluation")
async def update_dataset_evaluation(data: UpdateEvalData):
    try:
        results = model.update_dataset_evaluation(
            del_roaster=data.del_roaster
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_students_dataset")
async def check_students_dataset():
    try:
        results = model.students_dataset_exists()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete_students_dataset")
async def delete_students_dataset():
    try:
        results = model.del_students_dataset()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_roaster_files")
async def check_roaster_files():
    try:
        results = model.roasters_exists()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/delete_roaster_files")
async def delete_roaster_files(data: DeleteRoasterData):
    try:
        results = model.del_roasters(user_id=data.user_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get_student_state_roaster")
async def get_student_state_roaster(data: DeleteRoasterData):
    try:
        results = model.get_student_state_roaster(user_id=data.user_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/get_model_status")
async def get_model_status(data: DeleteRoasterData):
    try:
        results = model.get_model_status()
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))