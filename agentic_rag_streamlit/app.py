import streamlit as st
import os
import fitz  # PyMuPDF for reading PDFs
import google.generativeai as genai

# Gemini API Key
GOOGLE_API_KEY = "AIzaSyDQf47Vdjfw7rfENXS5JQWPsQGVx30IVsU"
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-001")

st.set_page_config(page_title="Agentic RAG Chatbot", layout="centered")
 
st.title("📄 Agentic RAG Chatbot with Gemini API")
st.markdown("Upload a document and ask a question based on its contents.")

# Upload document
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Input question
question = st.text_input("Ask a question based on the document:", "")

# Read content from PDF
def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# Handle query
if st.button("Submit"):
    if uploaded_file and question:
        with st.spinner("Reading document and querying Gemini..."):
            doc_text = read_pdf(uploaded_file)

            prompt = f"""
You are a document assistant chatbot. Use the following document context to answer the user's question.

Document:
\"\"\"
{doc_text}
\"\"\"

User Question:
\"\"\"
{question}
\"\"\"

Give a clear and helpful answer based only on the document.
"""

            try:
                response = model.generate_content(prompt)
                st.success("Response:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Error from Gemini API: {str(e)}")
    else:
        st.warning("Please upload a PDF and enter a question.")
