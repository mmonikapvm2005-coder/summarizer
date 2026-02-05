import streamlit as st
from groq import Groq
import os
from docx import Document
from PyPDF2 import PdfReader

st.set_page_config(page_title="Test Paper Analyzer", layout="centered")

st.title("Test Paper Analysis")
st.write("Upload a test paper (PDF, Word, or Text) to analyze its quality and difficulty.")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")

    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

uploaded_file = st.file_uploader(
    "Upload Test Paper",
    type=["txt", "pdf", "docx"]
)

if uploaded_file:
    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("Could not extract text from the file.")
    else:
        st.subheader("Extracted Content (Preview)")
        st.text_area("Test Paper", text, height=250)

        if st.button("Analyze Test Paper"):
            with st.spinner("Analyzing test paper..."):
                prompt = f"""
You are an academic assessment expert.

Analyze the following test paper and provide:
1. Types of questions
2. Estimated difficulty level
3. Topics or subjects covered
4. Bloom’s taxonomy levels involved
5. Overall quality and improvement suggestions

Test Paper Content:
{text}
"""

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You analyze exam question papers."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=700
                )

                analysis = response.choices[0].message.content

                st.success("Analysis Complete")
                st.markdown(analysis)
