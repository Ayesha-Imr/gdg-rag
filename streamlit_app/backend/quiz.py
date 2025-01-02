# quiz.py

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

if not os.getenv("COHERE_API_KEY"):
    os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

# Define Quiz Schema
class Quiz(BaseModel):
    questions: List[str] = Field(description="List of quiz questions.")
    answers: List[str] = Field(description="List of corresponding answers to the quiz questions.")

# Document Loading
def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            print(f"Unsupported file type: {filename}")
            continue
        documents.extend(loader.load())
    return documents

# Embedding and Vector Store Setup
def setup_vectorstore(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    splits = text_splitter.split_documents(documents)

    from langchain_cohere import CohereEmbeddings
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    vectorstore = Chroma.from_documents(
        collection_name="my_collection",
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db",
    )
    return vectorstore

# Quiz Generation Chain
def create_quiz_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
    quiz_llm = llm.with_structured_output(Quiz)

    quiz_template = """
    Based on the following content, generate a quiz with questions and corresponding answers.

    Content:
    {context}

    The output should be in JSON format with two keys: 'questions' and 'answers'.
    """
    quiz_prompt = ChatPromptTemplate.from_template(quiz_template)

    def docs_to_string(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | docs_to_string, "question": RunnablePassthrough()}
        | quiz_prompt
        | quiz_llm
    )

# Generate Quiz
def generate_quiz(vectorstore, topic):
    quiz_chain = create_quiz_chain(vectorstore)
    res = quiz_chain.invoke(topic)
    print(res)
    return res
