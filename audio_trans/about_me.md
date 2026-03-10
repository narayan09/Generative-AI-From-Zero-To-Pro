# 🎙️ AI Meeting Audio → MOM Generator

An **AI-powered meeting assistant** that converts meeting audio into **structured Minutes of Meeting (MOM)** with bullet points,  action items, risks, and next steps.

This project uses **open-source speech-to-text** and **LLM summarization** to automatically analyze meeting recordings.

---

# 🚀 Features

* 🎧 Convert meeting **audio → transcript**
* 🧠 Generate **structured meeting summaries**
* 📌 Extract **Action Items**
* ⚠️ Identify **Risks / Blockers**
* 📋 Generate **professional MOM format**
* ⚡ Fast LLM inference using Groq

---

# 🏗️ Architecture

```
Meeting Audio (.m4a / .mp3 / .wav)
            │
            ▼
   Speech-to-Text (Whisper)
            │
            ▼
      Transcript Text
            │
            ▼
   LangChain Prompt Template
            │
            ▼
      Groq LLM (Llama 3)
            │
            ▼
 Structured Minutes of Meeting
```

---

# 🧰 Tech Stack

| Tool           | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Core programming language    |
| OpenAI Whisper | Speech-to-text transcription |
| LangChain      | LLM orchestration            |
| Groq API       | Ultra-fast LLM inference     |
| Llama 3 Model  | Meeting summarization        |
| FFmpeg         | Audio decoding               |

---

# 📂 Project Structure

```
ai-meeting-mom/
│
├── meeting_audio/                # Sample meeting recordings
│   └── March_release.m4a
│
├── src/
│   └── meeting_summarizer.py     # Main application script
│
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/ai-meeting-mom.git
cd ai-meeting-mom
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

### Mac / Linux

```
source venv/bin/activate
```

### Windows

```
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

# 📦 Requirements

Example `requirements.txt`

```
openai-whisper
langchain
langchain-groq
python-dotenv
ffmpeg-python
torch
```

---

# 🎧 Install FFmpeg

The transcription library requires **FFmpeg**.

## Ubuntu / Linux

```
sudo apt update
sudo apt install ffmpeg
```

## Mac

```
brew install ffmpeg
```

## Windows

Download from:

https://ffmpeg.org/download.html

Add FFmpeg to **System PATH**.

Verify installation:

```
ffmpeg -version
```

---

# 🔑 Setup Groq API Key

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

Get your API key from the **Groq Console**.

---

# ▶️ Running the Project

Run the script:

```
python src/meeting_summarizer.py
```

Input audio example:

```
March_release.m4a
```

---

# 🧠 Example Prompt Used

The AI converts transcripts into structured MOM.

```
You are an expert AI meeting assistant.

Analyze the meeting transcript and generate:

Meeting Objective
Meeting Summary
Key Discussion Points
Decisions Taken
Action Items
Risks / Blockers
Next Steps
```

---

# 📊 Example Output

```
Meeting Objective
• Discuss the March product release plan

Meeting Summary
• Backend API development starts next week
• UI design completion by Friday

Key Discussion Points
• API development timeline
• UI completion schedule



Decisions Taken
• March release scheduled for end of month

Action Items
• Backend team to start API development

Risks / Blockers
• API specifications pending

Next Steps
• Follow-up meeting next Monday
```

---

# 🎧 Supported Audio Formats

```
mp3
wav
m4a
mp4
flac
aac
ogg
```

---

# 📈 Future Improvements

Planned enhancements:

* 👥 Speaker diarization
* 📊 Topic segmentation
* 📅 Calendar integration
* 📧 Email MOM automatically
* 📄 Export summary to PDF
* 🌐 Streamlit Web UI
* 📌 Jira ticket generation

---

# 🧪 Sample Meeting Audio

Place your meeting audio inside:

```
meeting_audio/
```

Example:

```
meeting_audio/March_release.m4a
```

---

# 🛠️ Troubleshooting

### FFmpeg not found

Install FFmpeg and verify:

```
ffmpeg -version
```

---

### Whisper slow on CPU

Use smaller model:

```
whisper.load_model("base")
```

Instead of:

```
whisper.load_model("medium")
```

---

# 🔐 Environment Variables

Example `.env`

```
GROQ_API_KEY=your_api_key_here
```

Never commit `.env` to GitHub.


---

# 👨‍💻 Author

Developed by **Narayan Mishra**

Python Developer | AI Enthusiast

---

# ⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork the repository
🛠️ Contribute improvements

---

# 💡 Inspiration

This project is inspired by AI meeting tools such as:

* Otter.ai
* Fireflies.ai

but built using **open-source tools and Groq LLM inference**.
