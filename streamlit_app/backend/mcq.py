import os
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from backend.quiz import setup_vectorstore

# Define MCQ Schema
class MCQ(BaseModel):
    """Model representing a multiple-choice question."""
    question: str = Field(description="The question text.")
    choices: List[str] = Field(description="List of 4 possible answers for the question.")
    correct_answer: str = Field(description="The correct answer for the question.")

class MCQQuiz(BaseModel):
    """Model representing a quiz with multiple-choice questions."""
    mcqs: List[MCQ] = Field(description="List of multiple-choice questions.")

# MCQ Generation Chain
def create_mcq_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
    mcq_llm = llm.with_structured_output(MCQQuiz)

    mcq_template = """
    Based on the following content, generate a set of multiple-choice questions (MCQs). Each question should include:
    1. A question text.
    2. A list of 4 choices, including the correct answer and 3 distractors.
    3. The correct answer.

    The output should be in JSON format with the following structure:
    {{
        "mcqs": [
            {{
                "question": "Question text here",
                "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                "correct_answer": "The correct choice here"
            }},
            ...
        ]
    }}

    Content:
    {context}
    """
    mcq_prompt = ChatPromptTemplate.from_template(mcq_template)

    def docs_to_string(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | docs_to_string, "question": RunnablePassthrough()}
        | mcq_prompt
        | mcq_llm
    )

# Generate MCQs
def generate_mcqs(vectorstore, topic):
    mcq_chain = create_mcq_chain(vectorstore)
    res = mcq_chain.invoke(topic)
    print(res)
    return res
