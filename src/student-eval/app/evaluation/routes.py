from fastapi import APIRouter
from src.common.controllers.evaluation_results_controller import EvaluationResultsController
from src.common.services.evaluations_service import EvaluationSQLServerService
from .models import SomeRandomModel

# Initialize the evaluation results service
evaluation_results_service = EvaluationSQLServerService()
# Initialize the evaluation results controller with the service
controller = EvaluationResultsController(evaluation_results_service)
router = APIRouter(prefix="/evaluation")

@router.get("/")
async def get_evaluations():
    """
    Endpoint to get evaluation data.
    """
    return controller.get_evaluation_result("some_id")

@router.post("/")
async def process_data(data: dict):
    """
    Endpoint to process evaluation data.
    """
    # Process of the answer given by the student to assess the evaluation
    evaluation_model = SomeRandomModel()
    evaluation_model.evaluate(data)

    # Call the controller to save the evaluation result
    controller.create_evaluation_result(data)
    return {"message": "Data processed successfully.", "data": data}