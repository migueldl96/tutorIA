from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class InitialEvaluationDTO:
    """Data Transfer Object for Initial Evaluation."""
    student_id: str
    evaluation_date: datetime
    subject: str
    score: float
    notes: Optional[str] = None 