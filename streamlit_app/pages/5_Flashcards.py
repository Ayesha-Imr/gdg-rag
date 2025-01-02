import streamlit as st
from backend.flashcards import setup_vectorstore, generate_flashcards

st.set_page_config(page_title="Generate Flashcards", page_icon="📝", layout="wide")

st.title("Generate Flashcards 📝")

# Ensure documents are uploaded
if "documents" not in st.session_state:
    st.error("No documents uploaded! Please go to the 'Upload Files' page and upload documents first.")
else:
    # Topic input
    topic = st.text_input("Enter a topic for the flashcards:", autocomplete="off")

    # State for storing flashcard data
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = None

    # Generate button
    if st.button("Generate Flashcards"):
        if not topic:
            st.warning("Please enter a topic!")
        else:
            # Backend processing
            with st.spinner("Generating the flashcards..."):
                vectorstore = setup_vectorstore(st.session_state.documents)
                st.session_state.flashcards = generate_flashcards(vectorstore, topic)

    # Display flashcards if available
    if st.session_state.flashcards:
        flashcards = st.session_state.flashcards

        st.subheader("Flashcards")
        st.markdown(
            """
            <style>
                .flashcard-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    gap: 30px; /* Increased spacing between cards */
                    margin-top: 20px;
                }
                .flashcard {
                    width: 60%; /* Narrower cards */
                    max-width: 500px; /* More defined max width */
                    height: auto; /* Adjust card height dynamically */
                    min-height: 150px; /* Ensures a good vertical height */
                    border: 2px solid #ccc;
                    padding: 30px; /* More padding for better readability */
                    border-radius: 12px;
                    background-color: #f9f9f9;
                    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1); /* Slightly deeper shadow for better appearance */
                }
                .flashcard h4 {
                    font-size: 1.8rem; /* Larger font for title */
                    color: #333;
                    margin-bottom: 15px;
                }
                .flashcard p {
                    font-size: 1.4rem; /* Increased font size for content */
                    color: #555;
                    line-height: 1.8;
                    margin: 0; /* Remove default paragraph margins */
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="flashcard-container">', unsafe_allow_html=True)
        for i, card in enumerate(flashcards, start=1):
            st.markdown(
                f"""
                <div class="flashcard">
                    <h4>Flashcard {i}</h4>
                    <p>{card}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
