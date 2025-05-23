import json
import os
import pickle
from typing import List, Optional, TypeVar, Generic, Type
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from .base_repository import BaseRepository


class AzureBlobRepository(BaseRepository):
    def __init__(self, container_name: str):
        load_dotenv()
        self.connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # instantiate the blob service client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def get_file(self, file_name: str) -> bytes:
        """Retrieve a file from the repository."""
        try:
            # Get blob client and download the blob
            blob_client = self.container_client.get_blob_client(file_name)
            blob_data = blob_client.download_blob().readall()
            
            # Convert bytes to string and return
            return blob_data
        except Exception as e:
            raise Exception(f"Error retrieving file {file_name}: {str(e)}")
        
    def save_file(self, file_name: str, file_content: bytes):
        """Save a file to the repository."""
        try:
            # Get blob client and upload the blob
            blob_client = self.container_client.get_blob_client(file_name)
            result = blob_client.upload_blob(file_content, overwrite=True)
        except Exception as e:
            raise Exception(f"Error saving file {file_name}: {str(e)}")
        
    def file_exists(self, file_name: str) -> bool:
        """Check if a file exists in the repository."""
        try:
            blob_client = self.container_client.get_blob_client(file_name)
            return blob_client.exists()
        except Exception as e:
            raise Exception(f"Error checking if file {file_name} exists: {str(e)}")
    def delete_file(self, file_name: str):
        """Delete a file from the repository."""
        try:
            blob_client = self.container_client.get_blob_client(file_name)
            blob_client.delete_blob()
        except Exception as e:
            raise Exception(f"Error deleting file {file_name}: {str(e)}")