import streamlit as st # pyright: ignore[reportMissingImports]
from parse_csv import parse_csv # type: ignore
from parse_resume import parse_resumes # pyright: ignore[reportMissingImports]
from score_candidates import score_candidate # type: ignore
from outreach import generate_message # type: ignore
from ai_interview import ai_interview # type: ignore

st.title("AI Hiring Dashboard")

# Upload CSV or choose PDF folder
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
use_pdf = st.sidebar.checkbox("Use PDF resumes in data/resumes")

candidates = []

if uploaded_file:
    candidates = parse_csv(uploaded_file)
elif use_pdf:
    candidates = parse_resumes()

if candidates:
    for c in candidates:
        c['score'] = score_candidate(c['text'])
    top_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
    for c in top_candidates[:10]:
        st.subheader(c['name'])
        st.write(f"Score: {c['score']:.2f}")
        st.write("AI Outreach Message:")
        st.write(generate_message(c['name']))
        st.write("AI Interview Summary:")
        st.write(ai_interview(c['name'], c['text']))
        st.write("---")
else:
    st.info("Upload CSV or select PDF resumes to start.")
