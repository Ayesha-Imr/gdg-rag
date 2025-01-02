import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend.quiz import setup_vectorstore
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

# Q&A Chain Setup
def create_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template)

    def docs2str(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | docs2str, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

# Generate Answer
def generate_answer(vectorstore, question):
    qa_chain = create_qa_chain(vectorstore)
    return qa_chain.invoke(question)
