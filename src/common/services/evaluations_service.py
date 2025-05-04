from .base_service import BaseService
from src.common.dto.evaluation_result import InitialEvaluationDTO

class EvaluationSQLServerService(BaseService):
    """
    Service class for managing evaluations in a SQL Server database.
    This class implements the CRUD operations defined in the BaseService class.
    """

    def create(self, data: InitialEvaluationDTO):
        """
        Create a new evaluation record in the SQL Server database.
        :param data: The evaluation data to create.
        :return: The created evaluation record.
        """
        # Implementation for creating an evaluation record in SQL Server
        pass

    def read(self, resource_id: str):
        """
        Read an evaluation record by its ID from the SQL Server database.
        :param resource_id: The ID of the evaluation record to read.
        :return: The evaluation record data.
        """
        # Implementation for reading an evaluation record from SQL Server
        pass

    def update(self, resource_id: str, data: InitialEvaluationDTO):
        """
        Update an evaluation record by its ID in the SQL Server database.
        :param resource_id: The ID of the evaluation record to update.
        :param data: The new evaluation data.
        :return: The updated evaluation record.
        """
        # Implementation for updating an evaluation record in SQL Server
        pass

    def delete(self, resource_id: str):
        """
        Delete an evaluation record by its ID from the SQL Server database.
        :param resource_id: The ID of the evaluation record to delete.
        :return: None
        """
        # Implementation for deleting an evaluation record from SQL Server
        pass