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
You are an expert AI assistant specialized in analyzing Knowledge Transfer (KT) sessions.

Your task is to convert the given KT session transcript into a structured, actionable, and easy-to-follow document.

Follow a clear logical flow so that a new team member can understand the system/process without attending the session.

Return the output strictly in the following format:

KT Session Objective:
- Clearly describe what knowledge or system was explained

System / Process Overview:
- High-level explanation of the system, workflow, or topic discussed

Step-by-Step Flow:
- Provide a sequential flow of the process
- Use numbered steps
- Keep it simple and easy to follow

Key Components / Modules:
- List important components, tools, services, or modules discussed
- Provide short descriptions for each

Technical Details:
- Important commands, scripts, APIs, configurations, or logic explained
- Include examples if mentioned

Dependencies / Prerequisites:
- List required tools, access, environment setup, or permissions

Issues / Challenges Discussed:
- Any problems, limitations, or concerns raised

Resolutions / Suggestions:
- Solutions or recommendations provided during the session

Action Items:
- Clearly defined tasks
- Mention owner (person/team) if available
- Mention priority if possible (High/Medium/Low)

Risks / Blockers:
- Any risks that may impact implementation or understanding

Next Steps / Follow-ups:
- What needs to be done next
- Any planned follow-up sessions

Key Takeaways:
- 3–5 concise points summarizing the most important learnings

Transcript:
{transcript}
"""
)

# -------------------------
# Create LangChain Chain
# -------------------------
chain = prompt | llm


# -------------------------
# Generate MOM + Save File
# -------------------------
def generate_mom(audio_file):

    transcript = transcribe_audio(audio_file)

    print("\nTRANSCRIPT:\n")
    print(transcript)

    response = chain.invoke({
        "transcript": transcript
    })

    mom_output = response.content

    # -------------------------
    # Create output file name
    # -------------------------
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    output_file = f"{base_name}.txt"

    # -------------------------
    # Save to text file
    # -------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("===== TRANSCRIPT =====\n\n")
        f.write(transcript)
        f.write("\n\n===== MOM SUMMARY =====\n\n")
        f.write(mom_output)

    print(f"\n✅ Output saved to: {output_file}")

    return mom_output


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":

    audio_file = "Ams_esb.m4a"

    mom = generate_mom(audio_file)

    print("\n===== MOM SUMMARY =====\n")
    print(mom)