from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.content_generator.app.controllers.quiz_controller import QuizController
from src.content_generator.app.dto.quiz import Quiz, QuizQuestionWithURI

quiz_router = APIRouter(prefix="/quiz", tags=["quiz"])

class QuizGenerationRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5

class QuizEvaluationRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: str

def get_quiz_controller() -> QuizController:
    return QuizController()

@quiz_router.post("/generate", response_model=list[QuizQuestionWithURI])
async def generate_quiz(
    request: QuizGenerationRequest,
    controller: QuizController = Depends(get_quiz_controller)
):
    """
    Generate a quiz based on the given topic, difficulty, and number of questions.
    """
    return controller.generate_quiz(
        topic=request.topic,
        difficulty=request.difficulty,
        num_questions=request.num_questions
    )
