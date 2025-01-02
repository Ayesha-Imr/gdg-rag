import streamlit as st

st.set_page_config(
    page_title="Study Space",
    page_icon="📝",
    layout="centered",
)

st.header("Welcome to the Study Space App! 🎓")
st.subheader("Powered by Gen AI and RAG")

st.write(
    """
    This application allows you to:
    - Upload your study documents and save them into vector knowledgebase.
    - Ask questions and get answers based on the uploaded documents.
    - Generate quizzes based on a specific topic.
    - Generate multiple-choice questions (MCQs) based on a specific topic.
    - Generate flashcards based on a specific topic.
    
    Navigate to the appropriate page from the sidebar to get started. 
    You will need to upload your study documents first before using the other functionalities.
    Have fun studying! 🚀
    """
)
