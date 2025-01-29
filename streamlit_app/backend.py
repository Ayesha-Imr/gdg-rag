import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

# Function to load documents
def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            continue
        documents.extend(loader.load())
    return documents

# Function to split documents
def split_documents(documents: List[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_documents(documents)

# Function to create embeddings
def create_embeddings(splits):
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
    document_embeddings = embeddings.embed_documents([split.page_content for split in splits])
    return embeddings, document_embeddings

# Function to store embeddings in vector database
def store_embeddings(splits, embeddings):
    vectorstore = Chroma.from_documents(
        collection_name="my_collection",
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vectorstore

# Function to create RAG retriever
def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 2})

# Function to create RAG chain
def create_rag_chain(retriever):
    groq_api_key = os.getenv("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = groq_api_key
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
    
    prompt_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer: """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    def docs2str(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | docs2str, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain