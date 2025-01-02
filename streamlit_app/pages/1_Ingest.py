import streamlit as st
import os
from backend.quiz import load_documents

st.set_page_config(page_title="Upload Files", page_icon="📄", layout="wide")

st.title("Upload Your Files 📄")

# File upload section
st.subheader("Upload your documents")
uploaded_files = st.file_uploader("Choose your documents (PDF/DOCX)", accept_multiple_files=True, type=["pdf", "docx"])

if uploaded_files:
    # Save uploaded files to a temporary directory
    folder_path = "./uploaded_files"
    os.makedirs(folder_path, exist_ok=True)
    for file in uploaded_files:
        with open(os.path.join(folder_path, file.name), "wb") as f:
            f.write(file.getbuffer())

    # Load documents and store them in session state
    with st.spinner("Processing your documents..."):
        documents = load_documents(folder_path)
        st.session_state.documents = documents
    st.success(f"Successfully uploaded and processed {len(uploaded_files)} files!")
else:
    st.info("Please upload your documents to proceed.")
