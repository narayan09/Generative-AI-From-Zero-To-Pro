import os
import whisper
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# -------------------------
# Load Whisper model
# -------------------------
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")


# -------------------------
# Transcribe Audio
# -------------------------
def transcribe_audio(audio_file):

    print("Transcribing audio...")

    result = whisper_model.transcribe(audio_file)

    return result["text"]


# -------------------------
# Setup Groq LLM
# -------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key,
    temperature=0
)


# -------------------------
# Prompt Template
# -------------------------
prompt = ChatPromptTemplate.from_template(
"""
You are an expert AI meeting assistant.

Analyze the following meeting transcript and generate structured Minutes of Meeting (MOM).

Return the output strictly in the following format:

Meeting Objective:
- Short description of the purpose of the meeting

Meeting Summary:
- Bullet point summary of the discussion

Key Discussion Points:
- Important topics discussed in the meeting


Decisions Taken:
- List any decisions made during the meeting

Action Items:
- Bullet points
- Include responsible person/team if mentioned

Risks / Blockers:
- Any risks or blockers discussed

Next Steps:
- Upcoming tasks or meetings

Transcript:
{transcript}
"""
)


# -------------------------
# Create LangChain Chain
# -------------------------
chain = prompt | llm


# -------------------------
# Generate MOM
# -------------------------
def generate_mom(audio_file):

    transcript = transcribe_audio(audio_file)

    print("\nTRANSCRIPT:\n")
    print(transcript)

    response = chain.invoke({
        "transcript": transcript
    })

    return response.content


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":

    audio_file = "March release.m4a"

    mom = generate_mom(audio_file)

    print("\n===== MOM SUMMARY =====\n")
    print(mom)