from src.common.services.evaluations_service import BaseService
from src.common.dto.evaluation_result import InitialEvaluationDTO
class EvaluationResultsController:
    """
    Controller for managing evaluation results. It interacts with the evaluation results service to fetch and save results.
    """
    def __init__(self, evaluation_results_service: BaseService):
        self._evaluation_results_service = evaluation_results_service

    
    def create_evaluation_result(self, data: InitialEvaluationDTO):
        """
        Create a new evaluation result.
        :param data: The data to create the evaluation result.
        :return: The created evaluation result.
        """
        return self._evaluation_results_service.create(data)
    
    def get_evaluation_result(self, resource_id: str):
        """
        Get an evaluation result by its ID.
        :param resource_id: The ID of the evaluation result to get.
        :return: The evaluation result data.
        """
        return self._evaluation_results_service.read(resource_id)