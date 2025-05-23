from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

class BaseRepository(ABC):
    """Base repository interface that defines common operations for all repositories."""
    
    @abstractmethod
    async def get_file(self, file_name: str) -> str:
        """Retrieve a file from the repository."""
        pass

    @abstractmethod
    async def save_file(self, file_name: str, file_content: bytes):
        """Save a file to the repository."""
        pass

    @abstractmethod
    async def file_exists(self, file_name: str) -> bool:
        """Check if a file exists in the repository."""
        pass