import openai # type: ignore
openai.api_key = "YOUR_OPENAI_API_KEY"

def ai_interview(candidate_name, candidate_text):
    prompt = f"""
    You are an AI interviewer. Evaluate {candidate_name} based on the resume below.
    Give scores from 1-10 for:
    - Technical skills
    - Communication
    - Suitability for AI & Automation Engineer role
    Provide a short summary with strengths and areas to improve.
    Resume: {candidate_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content
