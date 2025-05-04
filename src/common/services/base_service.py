from abc import ABC, abstractmethod
from src.common.dto.evaluation_result import InitialEvaluationDTO
class BaseService(ABC):
    """
    Base class for all evaluation services in the application.
    This class defines the basic CRUD operations that all services should implement, independent of the specific resource they manage.
    """

    @abstractmethod
    def create(self, data: InitialEvaluationDTO):
        """
        Create a new resource.
        :param data: The data to create the resource.
        :return: The created resource.
        """
        pass
    @abstractmethod
    def read(self, resource_id: str):
        """
        Read a resource by its ID.
        :param resource_id: The ID of the resource to read.
        :return: The resource data.
        """
        pass
    @abstractmethod
    def update(self, resource_id: str, data: InitialEvaluationDTO):
        """
        Update a resource by its ID.
        :param resource_id: The ID of the resource to update.
        :param data: The new data for the resource.
        :return: The updated resource.
        """
        pass
    @abstractmethod
    def delete(self, resource_id: str):
        """
        Delete a resource by its ID.
        :param resource_id: The ID of the resource to delete.
        :return: None
        """
        pass