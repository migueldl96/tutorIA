import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.content_generator.app.services.aisearch_service import AzureAISearchService
from src.content_generator.app.dto.quiz import Quiz, QuizQuestionWithURI
from src.content_generator.app.controllers.prompt_templates import SYSTEM_PROMPT, USER_PROMPT
import random

class SkillContext:
    def __init__(self, skill: str, content: str, difficulty: str, filename: str, page_number: int):
        """
        Initialize a SkillContext object.
        Args:
            skill (str): The skill associated with the context
            content (str): The content related to the skill
            difficulty (str): The difficulty level of the content
            filename (str): The name of the file where the content is stored
            page_number (int): The page number in the file where the content is located
        """


        self.skill = skill
        self.content = content
        self.difficulty = difficulty
        self.filename = filename
        self.page_number = page_number

class QuizController:
    def __init__(self):
        load_dotenv()

        # Initialize Azure OpenAI client
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
            seed=random.randint(0, 10000)  # Random seed for reproducibility
        )
        
        # Initialize output parser
        self.structured_output_llm = self.llm.with_structured_output(Quiz)

        search_service = AzureAISearchService()



     
    def generate_quiz(
        self,
        topic: str,
        difficulty: str = "medium",
        num_questions: int = 5
    ) -> list[QuizQuestionWithURI]:
        """
        Generate a quiz based on the given topic, difficulty, and number of questions.
        
        Args:
            topic (str): The topic for the quiz
            difficulty (str): The difficulty level (easy, medium, hard)
            num_questions (int): Number of questions to generate
            
        Returns:
            Quiz: A Quiz object containing the generated questions
        """
         # Get the context for the topic
        skills_contexts = self._get_skill_context([topic])
        # Prepare the skills context for the prompt
        skills_contexts_str = "\n".join(
            f"Skill: {skill_context.skill}, Difficulty: {skill_context.difficulty}, "
            f"Content: {skill_context.content}, Page: {skill_context.page_number}, "
            f"Filename: {skill_context.filename}"
            for skill_context in skills_contexts
        )
        skill_names_str = ", ".join(skill_context.skill for skill_context in skills_contexts)


        prompt_format = {
            "skill_names": skill_names_str,
            "skills_contexts": skills_contexts_str,
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
        
        # Add the URI to each question
        prefix_uri = "https://tutoriastoragesa.blob.core.windows.net/temario/"
        questions_with_uri = []
        for question in response.quiz:
            # Create a QuizQuestionWithURI object
            question_with_uri : QuizQuestionWithURI = QuizQuestionWithURI(
                **question.model_dump(),  # Unpack the original question
                uri=f"{prefix_uri}{question.filename}"  # Initialize URI as an empty string
            )
            questions_with_uri.append(question_with_uri)
        # Return the generated quiz
        return questions_with_uri

    def _get_skill_context(self, skills: list[str]) -> list[SkillContext]:
        """
        Get context for a specific skill using Azure AI Search.
        Args:
            skill (str): The skill to search for
        Returns:
            str: Contextual information about the skill
        """
        search_service = AzureAISearchService()
        skill_contexts = []
        for skill in skills:
            results = search_service.search_by_skill(skill, top=5)
            for result in results:
                # Create a SkillContext object for each result
                skill_context = SkillContext(
                    skill=skill,
                    content=result.get("content", ""),
                    difficulty=result.get("difficulty", "medium"),
                    filename=result.get("filename", ""),
                    page_number=result.get("page_number", 0)
                )
                skill_contexts.append(skill_context)

        return skill_contexts