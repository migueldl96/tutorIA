from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.content_generator.app.services.aisearch_service import AzureAISearchService

router = APIRouter(prefix="/search", tags=["search"])

# Initialize the search service
search_service = AzureAISearchService()

class SearchResponse(BaseModel):
    """Response model for search results."""
    results: List[Dict[str, Any]]
    total_results: int

class SearchRequest(BaseModel):
    """Request model for search parameters."""
    search_text: str
    skills: Optional[List[str]] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    top: int = 10

@router.get("/skill/{skill}", response_model=SearchResponse)
async def search_by_skill(
    skill: str,
    top: int = Query(10, ge=1, le=100)
) -> SearchResponse:
    """
    Search for documents containing a specific skill.
    
    Args:
        skill (str): The skill to search for
        top (int): Maximum number of results to return (1-100)
        
    Returns:
        SearchResponse: Search results and total count
    """
    try:
        results = search_service.search_by_skill(skill, top)
        return SearchResponse(
            results=results,
            total_results=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/subject/{subject}", response_model=SearchResponse)
async def search_by_subject(
    subject: str,
    top: int = Query(10, ge=1, le=100)
) -> SearchResponse:
    """
    Search for documents with a specific subject.
    
    Args:
        subject (str): The subject to search for
        top (int): Maximum number of results to return (1-100)
        
    Returns:
        SearchResponse: Search results and total count
    """
    try:
        results = search_service.search_by_subject(subject, top)
        return SearchResponse(
            results=results,
            total_results=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/difficulty/{difficulty}", response_model=SearchResponse)
async def search_by_difficulty(
    difficulty: str,
    top: int = Query(10, ge=1, le=100)
) -> SearchResponse:
    """
    Search for documents with a specific difficulty level.
    
    Args:
        difficulty (str): The difficulty level to search for
        top (int): Maximum number of results to return (1-100)
        
    Returns:
        SearchResponse: Search results and total count
    """
    try:
        results = search_service.search_by_difficulty(difficulty, top)
        return SearchResponse(
            results=results,
            total_results=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/combined", response_model=SearchResponse)
async def combined_search(request: SearchRequest) -> SearchResponse:
    """
    Perform a search with multiple filters.
    
    Args:
        request (SearchRequest): Search parameters including text and filters
        
    Returns:
        SearchResponse: Search results and total count
    """
    try:
        results = search_service.combined_search(
            search_text=request.search_text,
            skills=request.skills,
            subject=request.subject,
            difficulty=request.difficulty,
            top=request.top
        )
        return SearchResponse(
            results=results,
            total_results=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 