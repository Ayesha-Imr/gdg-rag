import streamlit as st
import os
from backend import load_documents, split_documents, create_embeddings, store_embeddings, get_retriever, create_rag_chain

def main():
    st.title("📄 RAG-based Document Chatbot")
    st.write("Welcome to the RAG-based Document Chatbot! 🤖")
    st.write("Upload PDF or Word documents and chat with them. 📚")
    st.write("---")

    # File uploader
    st.header("📤 Upload Documents")
    uploaded_files = st.file_uploader("Upload files", type=["pdf", "docx"], accept_multiple_files=True)
    
    if uploaded_files:
        folder_path = "uploaded_docs"
        os.makedirs(folder_path, exist_ok=True)
        
        for file in uploaded_files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        
        st.success("✅ Files uploaded successfully!")
        
        with st.spinner("⚙️ Processing documents..."):
            documents = load_documents(folder_path)
            splits = split_documents(documents)
            embeddings, _ = create_embeddings(splits)
            vectorstore = store_embeddings(splits, embeddings)
            retriever = get_retriever(vectorstore)
            rag_chain = create_rag_chain(retriever)
        
        st.session_state.rag_chain = rag_chain
        st.success("✅ Documents processed and ready for chat!")
        st.write("---")

    # Chat box
    if "rag_chain" in st.session_state:
        st.header("💬 Chat with Documents")
        question = st.text_input("Ask a question about the documents:", autocomplete="off")
        if question:
            with st.spinner("💬 Generating response..."):
                response = st.session_state.rag_chain.invoke(question)
                st.write("**Answer:**", response)

if __name__ == "__main__":
    main()