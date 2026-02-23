import openai # pyright: ignore[reportMissingImports]
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_message(candidate_name, role="AI & Automation Engineer"):
    prompt = f"Write a short, professional outreach message to {candidate_name} for the role of {role}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content
