from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class QuizQuestion(BaseModel):
    question: str = Field(..., description="The question of the quiz")
    optionA: str = Field(..., description="The first option of the question")
    optionB: str = Field(..., description="The second option of the question")
    optionC: str = Field(..., description="The third option of the question")
    optionD: str = Field(..., description="The fourth option of the question")
    correct_answer: str = Field(..., description="The correct answer of the question")
    explanation: Optional[str] = Field(..., description="Explanation of the correct answer")

class Quiz(BaseModel):
    quiz: List[QuizQuestion] = Field(..., description="List of quiz questions")

