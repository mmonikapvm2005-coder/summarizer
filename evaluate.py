import streamlit as st
from groq import Groq
import PyPDF2
import docx
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="LLM Exam Evaluator", layout="centered")
st.title("LLM-Based Answer Sheet Evaluation")

st.write("Upload student answers. The system will evaluate using AI.")

# ---------- Helper Functions ----------

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""

def evaluate_answers(student_text):
    prompt = f"""
You are an exam evaluator.

Question Paper:
Q1. What is an operating system? (5 marks)
Q2. Explain CPU and its functions. (5 marks)
Q3. What is FIFO? Give an example. (5 marks)

Model Answers:
Q1. An operating system manages hardware and software resources and provides services to programs.
Q2. CPU stands for Central Processing Unit. It performs arithmetic, logic, control and processing operations.
Q3. FIFO means First In First Out. Example: Queue.

Student Answers:
{student_text}

Instructions:
- Evaluate each answer strictly
- Give marks out of 5 for each question
- Provide short feedback
- Give total marks out of 15

Output format:
Q1: Marks = x/5 | Feedback = ...
Q2: Marks = x/5 | Feedback = ...
Q3: Marks = x/5 | Feedback = ...
Total = xx/15
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# ---------- UI ----------

uploaded_file = st.file_uploader(
    "Upload Student Answer Sheet (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    student_text = extract_text(uploaded_file)

    st.subheader("Extracted Student Answers")
    st.text_area("Answer Content", student_text, height=200)

    if st.button("Evaluate Answers"):
        with st.spinner("Evaluating using AI..."):
            result = evaluate_answers(student_text)

        st.divider()
        st.subheader("Evaluation Result")
        st.write(result)
