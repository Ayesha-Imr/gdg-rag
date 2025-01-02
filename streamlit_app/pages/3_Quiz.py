# quiz.py

import streamlit as st
import os
from backend.quiz import setup_vectorstore, generate_quiz

st.set_page_config(page_title="Generate Quiz", page_icon="📝", layout="wide")

st.title("Generate a Quiz 📝")

# Ensure documents are uploaded
if "documents" not in st.session_state:
    st.error("No documents uploaded! Please go to the 'Upload Files' page and upload documents first.")
else:
    # Topic input
    topic = st.text_input("Enter a topic for the quiz:", autocomplete="off")

    # State for storing quiz data
    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    # Generate button
    if st.button("Generate Quiz"):
        if not topic:
            st.warning("Please enter a topic!")
        else:
            # Backend processing
            with st.spinner("Generating the quiz..."):
                vectorstore = setup_vectorstore(st.session_state.documents)
                st.session_state.quiz = generate_quiz(vectorstore, topic)

    # Display quiz questions and answers if available
    if st.session_state.quiz:
        quiz = st.session_state.quiz

        # Display questions
        st.subheader("Quiz Questions")
        for i, question in enumerate(quiz.questions, start=1):
            st.write(f"{i}. {question}")

        # Collapsible section for answers
        with st.expander("Show Answers"):
            st.subheader("Answers")
            for i, answer in enumerate(quiz.answers, start=1):
                st.write(f"{i}. {answer}")
