import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from backend.quiz import setup_vectorstore

from pydantic import BaseModel, Field
from typing import List

class Flashcards(BaseModel):
    """Model representing flashcard content"""
    flashcard: List[str] = Field(description="List of concise, memorable flashcard content.")

# Flashcards Generation Chain
def create_flashcards_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

    cards_llm = llm.with_structured_output(Flashcards)

    flashcards_template = """
    Based on the following content, generate concise and memorable flashcards.

    Content:
    {context}

    The output should be in JSON format with the key: 'flashcard_content'.
    """
    flashcards_prompt = ChatPromptTemplate.from_template(flashcards_template)

    def docs_to_string(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | docs_to_string, "question": RunnablePassthrough()}
        | flashcards_prompt
        | cards_llm
    )

# Generate Flashcards
def generate_flashcards(vectorstore, topic):
    flashcards_chain = create_flashcards_chain(vectorstore)
    res = flashcards_chain.invoke(topic)
    print(res)
    return res.flashcard
