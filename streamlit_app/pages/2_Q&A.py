import streamlit as st
from backend.qna import setup_vectorstore, generate_answer

st.set_page_config(page_title="Ask Questions", page_icon="💬", layout="wide")

st.title("Ask Questions 💬")

# Ensure documents are uploaded
if "documents" not in st.session_state:
    st.error("No documents uploaded! Please go to the 'Upload Files' page and upload documents first.")
else:
    # State for storing the current question and answer
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # Input box for question
    question = st.text_input("Enter your question:", autocomplete="off")

    # Generate button
    if st.button("Get Answer"):
        if not question:
            st.warning("Please enter a question!")
        else:
            # Backend processing
            with st.spinner("Retrieving answer..."):
                vectorstore = setup_vectorstore(st.session_state.documents)
                answer = generate_answer(vectorstore, question)
                st.session_state.qa_history.append((question, answer))

    # Display Q&A history
    if st.session_state.qa_history:
        st.subheader("Q&A History")
        for i, (q, a) in enumerate(st.session_state.qa_history, start=1):
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 10px; background-color: #f9f9f9;">
                    <strong>Q{i}: {q}</strong>
                    <p style="margin-top: 10px;">A{i}: {a}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
