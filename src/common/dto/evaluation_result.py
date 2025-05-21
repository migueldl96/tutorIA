from pydantic import BaseModel
from typing import Dict, List, Any

class InitialEvaluationDTO(BaseModel):
    user_id: str
    skills_states: Dict[str, Dict[str, Any]] = {}
    students_states: Dict[str, Dict[str, Any]] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "alice",
                "skills_states": {
                    "math": {
                        "algebra": {
                            "prior": 0.0,
                            "learns": 0.2,
                            "forgets": 0.0
                        }
                    }
                },
                "students_states": {
                    "alice": {
                        "learns": {
                            "math": {"algebra": 0.2}
                        },
                        "forgets": {
                            "math": {"algebra": 0.0}
                        }
                    }
                }
            }
        }