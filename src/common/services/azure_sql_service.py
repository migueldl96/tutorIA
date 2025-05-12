from typing import Any, Dict, List, Optional
import pyodbc
from .base_service import BaseService
from src.common.dto.initial_evaluation_dto import InitialEvaluationDTO
import os 
from dotenv import load_dotenv

load_dotenv()

class AzureSQLService(BaseService):
    """Concrete implementation of BaseService for Azure SQL Server."""
    
    def __init__(self, connection_string: str = os.getenv("AZURE_SQL_CONNECTION_STRING")):
        """Initialize the Azure SQL Service.
        
        Args:
            connection_string: Azure SQL Server connection string
        """
        self.connection_string = connection_string
        self.connection = None
    
    async def connect(self) -> None:
        """Establish connection to Azure SQL Server."""
        try:
            self.connection = pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            raise ConnectionError(f"Failed to connect to Azure SQL Server: {str(e)}")
    
    async def disconnect(self) -> None:
        """Close the Azure SQL Server connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    async def create(self, data: InitialEvaluationDTO) -> Dict[str, Any]:
        """Create a new resource in Azure SQL Server.
        
        Args:
            data: The data to create the resource
            
        Returns:
            The created resource data
        """
        query = """
            INSERT INTO initial_evaluations (
                student_id, evaluation_date, subject, score, notes
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = {
            'student_id': data.student_id,
            'evaluation_date': data.evaluation_date,
            'subject': data.subject,
            'score': data.score,
            'notes': data.notes
        }
        
        result = await self.execute_query(query, params)
        return result[0] if result else None

    async def read(self, resource_id: str) -> Dict[str, Any]:
        """Read a resource by its ID from Azure SQL Server.
        
        Args:
            resource_id: The ID of the resource to read
            
        Returns:
            The resource data
        """
        query = "SELECT * FROM initial_evaluations WHERE id = ?"
        params = {'id': resource_id}
        
        result = await self.execute_query(query, params)
        return result[0] if result else None

    async def update(self, resource_id: str, data: InitialEvaluationDTO) -> Dict[str, Any]:
        """Update a resource by its ID in Azure SQL Server.
        
        Args:
            resource_id: The ID of the resource to update
            data: The new data for the resource
            
        Returns:
            The updated resource data
        """
        query = """
            UPDATE initial_evaluations 
            SET student_id = ?, evaluation_date = ?, subject = ?, score = ?, notes = ?
            WHERE id = ?
        """
        params = {
            'student_id': data.student_id,
            'evaluation_date': data.evaluation_date,
            'subject': data.subject,
            'score': data.score,
            'notes': data.notes,
            'id': resource_id
        }
        
        await self.execute_query(query, params)
        return await self.read(resource_id)

    async def delete(self, resource_id: str) -> None:
        """Delete a resource by its ID from Azure SQL Server.
        
        Args:
            resource_id: The ID of the resource to delete
        """
        query = "DELETE FROM initial_evaluations WHERE id = ?"
        params = {'id': resource_id}
        
        await self.execute_query(query, params)
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query on Azure SQL Server.
        
        Args:
            query: SQL query to execute
            params: Optional parameters for the query
            
        Returns:
            List of dictionaries containing the query results
        """
        if not self.connection:
            await self.connect()
            
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                
            return results
        except pyodbc.Error as e:
            raise Exception(f"Failed to execute query: {str(e)}")
        finally:
            cursor.close()
    
    async def execute_transaction(self, queries: List[Dict[str, Any]]) -> bool:
        """Execute multiple queries in a transaction on Azure SQL Server.
        
        Args:
            queries: List of dictionaries containing queries and their parameters
            
        Returns:
            True if transaction was successful, False otherwise
        """
        if not self.connection:
            await self.connect()
            
        try:
            cursor = self.connection.cursor()
            self.connection.autocommit = False
            
            for query_dict in queries:
                query = query_dict.get('query')
                params = query_dict.get('params')
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            self.connection.rollback()
            raise Exception(f"Transaction failed: {str(e)}")
        finally:
            self.connection.autocommit = True
            cursor.close() 