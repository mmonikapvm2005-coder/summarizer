import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Sentiment Analysis", layout="centered")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Sentiment Analysis")
st.write("Enter text below and analyze its sentiment.")

text = st.text_area("Text to analyze", height=180)

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        with st.spinner("Analyzing sentiment..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a sentiment analysis engine. "
                            "Classify the sentiment as Positive, Negative, or Neutral. "
                            "Then briefly explain why."
                        )
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.2,
                max_tokens=150
            )

            result = response.choices[0].message.content
            st.success("Analysis Complete")
            st.write(result)
