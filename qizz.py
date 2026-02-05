import streamlit as st

st.set_page_config(page_title="Online Test", layout="centered")

st.title("Online MCQ Test")
st.write("Select the correct answers and submit the test.")

# Questions data
questions = [
    {
        "question": "Which of the following is an operating system?",
        "options": ["MS Word", "Linux", "Chrome", "Oracle"],
        "answer": "Linux"
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Process Unit",
            "Central Processing Unit",
            "Computer Personal Unit",
            "Control Processing Unit"
        ],
        "answer": "Central Processing Unit"
    },
    {
        "question": "Which data structure follows FIFO?",
        "options": ["Stack", "Tree", "Queue", "Graph"],
        "answer": "Queue"
    },
    {
        "question": "Which language is used for web styling?",
        "options": ["HTML", "Python", "CSS", "Java"],
        "answer": "CSS"
    },
    {
        "question": "What is the full form of RAM?",
        "options": [
            "Random Access Memory",
            "Read Access Memory",
            "Rapid Action Memory",
            "Run Access Memory"
        ],
        "answer": "Random Access Memory"
    }
]

# Store answers
user_answers = {}

for i, q in enumerate(questions):
    st.subheader(f"Q{i+1}. {q['question']}")
    user_answers[i] = st.radio(
        "Choose one:",
        q["options"],
        key=f"q{i}"
    )

if st.button("Submit Test"):
    score = 0
    st.divider()
    st.subheader("Results")

    for i, q in enumerate(questions):
        correct = q["answer"]
        selected = user_answers[i]

        if selected == correct:
            score += 1
            st.success(f"Q{i+1}: Correct ✔ ({selected})")
        else:
            st.error(f"Q{i+1}: Incorrect ✘ (You chose: {selected})")
            st.info(f"Correct answer: {correct}")

    st.divider()
    st.subheader(f"Final Score: {score} / {len(questions)}")
