# Study-Space-RAG-Demo-App
A basic, beginner friendly RAG app for personalised study help.

# Study Space

Study Space is a basic, beginner friendly RAG app for personalised study help that allows you to interact with your uploaded documents. You can:

- Ask questions and get precise answers based on the document content.
- Generate quizzes to test your knowledge.
- Get MCQs to test your understanding.
- Create flashcards for learning and revision.

## Setup Instructions

Follow these steps to set up and run the app:

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
python -m venv myvenv
myvenv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### 3. Install the Requirements

Install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

The app requires two API keys:

1. **Cohere API Key**
   - Visit [Cohere API Key Page](https://dashboard.cohere.com/api-keys)
   - Log in or sign up to generate your free API key.

2. **Groq API Key**
   - Visit [Groq API Key Page](https://console.groq.com/keys)
   - Log in or sign up to generate your free API key.

Once you have both keys, do the following:

- Open the `env.txt` file in the root directory.
- Paste the API keys into the appropriate placeholders. The format should look like this:

```plaintext
COHERE_API_KEY="<your-cohere-api-key>"
GROQ_API_KEY="<your-groq-api-key>"
```

- Save the file and rename it to `.env` (remove the `.txt` extension).

### 5. Run the App

Navigate to the `streamlit-app` folder:

```bash
cd streamlit-app
```

Run the app using the following command:

```bash
streamlit run app.py
```

### 6. Access the App

After running the command, Streamlit will provide a local URL. Open the URL in your browser to start using Study Space.

---

That's it! Your app should now be running. If you encounter any issues, double-check the setup steps or refer to the relevant documentation for troubleshooting.

