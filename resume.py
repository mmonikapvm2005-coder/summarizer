import streamlit as st
from groq import Groq
import PyPDF2
import docx
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Resume Job Role Suggester", layout="centered")
st.title("AI Resume Job Description Suggester")

st.write("Upload your resume. The system will suggest the most suitable job role and description.")

# ---------- Helper Functions ----------

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

def suggest_job_description(resume_text):
    prompt = f"""
You are an expert technical recruiter and ATS specialist.

Analyze the resume content below and determine:
1. The most suitable job role for this candidate
2. A professional job description matching the candidate's skills
3. A brief explanation of why this role fits
4. 2 alternative job roles (if applicable)

Resume:
{resume_text}

Output format (strictly follow):

Recommended Job Title:
<job title>

Recommended Job Description:
<job description>

Why This Role Fits:
- ...

Alternative Roles:
- ...
- ...
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# ---------- UI ----------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    resume_text = extract_text(uploaded_file)

    st.subheader("Extracted Resume Content")
    st.text_area("Resume Text", resume_text, height=250)

    if st.button("Suggest Suitable Job Description"):
        with st.spinner("Analyzing resume and suggesting role..."):
            try:
                result = suggest_job_description(resume_text)
                st.divider()
                st.subheader("Job Role Recommendation")
                st.write(result)
            except Exception as e:
                st.error(f"Failed to analyze resume: {e}")

