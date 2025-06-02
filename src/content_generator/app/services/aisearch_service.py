from typing import List, Dict, Any, Optional
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import QueryType
import logging
import dotenv
# Load environment variables from .env file
dotenv.load_dotenv()

class AzureAISearchService:
    """Service for interacting with Azure AI Search."""
    
    def __init__(self):
        """Initialize the Azure AI Search service with credentials from environment variables."""
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "temario-index-v3")
        
        if not all([self.endpoint, self.key]):
            raise ValueError("Azure Search credentials not found in environment variables")
        
        self.credential = AzureKeyCredential(self.key)
        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential
        )
        
        logging.info(f"Initialized Azure AI Search service for index: {self.index_name}")

    def search(
        self,
        search_text: str,
        filter_expr: Optional[str] = None,
        select_fields: Optional[List[str]] = None,
        top: int = 10,
        skip: int = 0,
        query_type: QueryType = QueryType.SIMPLE
    ) -> List[Dict[str, Any]]:
        """
        Perform a search query with optional filtering.
        
        Args:
            search_text (str): The search query text
            filter_expr (str, optional): OData filter expression
            select_fields (List[str], optional): Fields to include in results
            top (int): Maximum number of results to return
            skip (int): Number of results to skip
            query_type (QueryType): Type of search query to perform
            
        Returns:
            List[Dict[str, Any]]: List of search results
        """
        try:
            results = self.search_client.search(
                search_text=search_text,
                filter=filter_expr,
                select=select_fields,
                top=top,
                skip=skip,
                query_type=query_type
            )
            
            return [dict(result) for result in results]
            
        except Exception as e:
            logging.error(f"Error performing search: {str(e)}")
            raise

    def search_by_skill(self, skill: str, top: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents that contain a specific skill.
        
        Args:
            skill (str): The skill to search for
            top (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of documents containing the skill
        """
        # Create filter expression for skills collection
        filter_expr = f"skills/any(s: s eq '{skill}')"
        
        return self.search(
            search_text="*",  # Match all documents
            filter_expr=filter_expr,
            select_fields=["content", "skills", "subject", "difficulty", "description", "filename", "page_number"],
            top=top
        )

    def search_by_subject(self, subject: str, top: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents with a specific subject.
        
        Args:
            subject (str): The subject to search for
            top (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of documents with the subject
        """
        filter_expr = f"subject eq '{subject}'"
        
        return self.search(
            search_text="*",
            filter_expr=filter_expr,
            select_fields=["content", "skills", "subject", "difficulty", "description", "filename", "page_number"],
            top=top
        )

    def search_by_difficulty(self, difficulty: str, top: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents with a specific difficulty level.
        
        Args:
            difficulty (str): The difficulty level to search for
            top (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of documents with the difficulty level
        """
        filter_expr = f"difficulty eq '{difficulty}'"
        
        return self.search(
            search_text="*",
            filter_expr=filter_expr,
            select_fields=["content", "skills", "subject", "difficulty", "description", "filename", "page_number"],
            top=top
        )

    def combined_search(
        self,
        search_text: str,
        skills: Optional[List[str]] = None,
        subject: Optional[str] = None,
        difficulty: Optional[str] = None,
        top: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform a search with multiple filters.
        
        Args:
            search_text (str): The search query text
            skills (List[str], optional): List of skills to filter by
            subject (str, optional): Subject to filter by
            difficulty (str, optional): Difficulty level to filter by
            top (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of filtered search results
        """
        filter_parts = []
        
        if skills:
            skill_filters = [f"skills/any(s: s eq '{skill}')" for skill in skills]
            filter_parts.append(f"({' or '.join(skill_filters)})")
            
        if subject:
            filter_parts.append(f"subject eq '{subject}'")
            
        if difficulty:
            filter_parts.append(f"difficulty eq '{difficulty}'")
            
        filter_expr = " and ".join(filter_parts) if filter_parts else None
        
        return self.search(
            search_text=search_text,
            filter_expr=filter_expr,
            select_fields=["content", "skills", "subject", "difficulty", "description", "filename", "page_number"],
            top=top
        )
