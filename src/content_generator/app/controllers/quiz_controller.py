import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.content_generator.app.dto.quiz import Quiz
from src.content_generator.app.controllers.prompt_templates import SYSTEM_PROMPT, USER_PROMPT

class QuizController:
    def __init__(self):
        load_dotenv()

        # Initialize Azure OpenAI client
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_GENERATOR_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        
        # Initialize output parser
        self.structured_output_llm = self.llm.with_structured_output(Quiz)


     
    def generate_quiz(
        self,
        topic: str,
        difficulty: str = "medium",
        num_questions: int = 5
    ) -> Quiz:
        """
        Generate a quiz based on the given topic, difficulty, and number of questions.
        
        Args:
            topic (str): The topic for the quiz
            difficulty (str): The difficulty level (easy, medium, hard)
            num_questions (int): Number of questions to generate
            
        Returns:
            Quiz: A Quiz object containing the generated questions
        """
        prompt_format = {
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions
        }

        # Get the system prompt
        system_prompt = SYSTEM_PROMPT

        # Get the user prompt
        user_prompt = USER_PROMPT

        # Create the chat message prompt
        chat_prompt : ChatPromptTemplate = ChatPromptTemplate.from_messages([
            system_prompt,
            user_prompt
        ])
        
        # Create the chain
        chain = chat_prompt | self.structured_output_llm

        # Run the chain
        response : Quiz = chain.invoke(input=prompt_format)
        
        return response
