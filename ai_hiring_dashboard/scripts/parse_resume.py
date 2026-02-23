import pdfplumber # type: ignore
import os

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_resumes(folder="data/resumes"):
    candidates = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            text = extract_text(os.path.join(folder, file))
            candidates.append({"name": file.replace(".pdf",""), "text": text})
    return candidates
