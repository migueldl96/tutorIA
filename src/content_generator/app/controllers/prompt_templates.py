from langchain.prompts import HumanMessagePromptTemplate, PromptTemplate, SystemMessagePromptTemplate

SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(
    """
            You are an expert educational assistant specialized in generating high-quality multiple-choice quizzes. 
            Your goal is to create well-structured quizzes that align with the requested topic and difficulty level.
            Each question must be clear, accurate, and informative, with plausible distractors and a concise explanation.
            Always respond with a JSON object in a predictable, consistent structure.
            Return the result as a well-formatted JSON object using the following structure:
            {{
            "quiz": [
                {{
                "question": "Your question here",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A/B/C/D",
                "explanation": "Explanation of the correct answer"
                }},
                ...
            ]
            }}
            Do NEVER add any commentary or extra text outside the JSON.
    """
)

USER_PROMPT = HumanMessagePromptTemplate.from_template(
    """
            Create a quiz using about the following skills:
            {skill_names}

            With the following difficulty levels and contexts:

            Skills and Contexts:
            {skills_contexts}

            If not empty, each context item in the list contains:
            - skill: The skill to assess
            - difficulty: The difficulty level
            - context: The content/context for the question
            - page_number: The page number from the source document
            - filename: The filename of the source document

            Generate exactly {num_questions} questions trying to cover all the skills and contexts provided. If there are not enough contexts, you can create questions based on the skills alone, but try not to stray too far from the content of the context.

            Each question must follow these guidelines:
            1. Be clear, concise, and relevant to the given skill, context, and difficulty.
            2. Provide exactly four answer choices labeled A, B, C, and D.
            3. Indicate the correct answer using the corresponding letter.
            4. Include a brief, informative explanation that justifies why the correct answer is right and, if helpful, why the others are incorrect.
            5. Add the context information used to generate the questions (skill, content, page number, filename).

            # Mandatory instructions:
            You must always use the context provided for each skill to generate the quiz questions. Be creative and ensure that the questions are educational and engaging, but always try to adhere to the skill and difficulty specified.

            Ensure that:
            - Each question is unique and aligned with the specified skill, context, and difficulty.
            - The output is valid JSON with no extra commentary.
    """
)

QUIZ_EVALUATION_TEMPLATE = PromptTemplate(
    input_variables=["question", "student_answer", "correct_answer"],
    template="""Evaluate the following answer to a quiz question:

    Question: {question}
    Student's Answer: {student_answer}
    Correct Answer: {correct_answer}

    Provide a brief evaluation of the student's answer, including:
    1. Whether the answer is correct
    2. A brief explanation of why it's correct or incorrect
    3. Suggestions for improvement if the answer is incorrect

    Format the response as a JSON object:
    {{
        "is_correct": true/false,
        "explanation": "explanation text",
        "suggestions": "improvement suggestions"
    }}
    """
) 