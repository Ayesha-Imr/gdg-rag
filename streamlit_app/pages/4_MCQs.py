import streamlit as st
from backend.mcq import setup_vectorstore, generate_mcqs

st.set_page_config(page_title="Generate MCQs", page_icon="📝", layout="wide")

st.title("Generate Multiple-Choice Questions (MCQs) 📝")

# Ensure documents are uploaded
if "documents" not in st.session_state:
    st.error("No documents uploaded! Please go to the 'Upload Files' page and upload documents first.")
else:
    # Topic input
    topic = st.text_input("Enter a topic for the MCQs:", autocomplete="off")

    # State for storing MCQ data
    if "mcqs" not in st.session_state:
        st.session_state.mcqs = None

    # Generate button
    if st.button("Generate MCQs"):
        if not topic:
            st.warning("Please enter a topic!")
        else:
            # Backend processing
            with st.spinner("Generating the MCQs..."):
                vectorstore = setup_vectorstore(st.session_state.documents)
                st.session_state.mcqs = generate_mcqs(vectorstore, topic)

    # Display MCQs if available
    if st.session_state.mcqs:
        mcqs = st.session_state.mcqs

        for i, mcq in enumerate(mcqs.mcqs, start=1):
            st.subheader(f"Question {i}: {mcq.question}")
            st.write("Choices:")
            for choice_idx, choice in enumerate(mcq.choices, start=1):
                st.write(f"{choice_idx}. {choice}")

            # Collapsible section for correct answer
            with st.expander("Show Correct Answer"):
                st.write(f"Correct Answer: {mcq.correct_answer}")
