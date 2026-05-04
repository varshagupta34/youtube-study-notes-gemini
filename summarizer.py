import os

from dotenv import load_dotenv
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables from .env
load_dotenv()

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def chunk_transcript(transcript: str, chunk_size: int = 8000) -> list:
    """Split long transcripts into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=500,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.split_text(transcript)


def generate_summary(transcript: str, style: str = "comprehensive") -> str:
    """Generate summary using Gemini Pro."""
    chunks = chunk_transcript(transcript)

    # If transcript fits in one call
    if len(chunks) == 1:
        return _summarize_single(transcript, style)

    # Map-reduce for long videos
    print(f"Long video detected — processing {len(chunks)} chunks...")
    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        summary = _summarize_single(chunk, "brief")
        chunk_summaries.append(summary)

    # Combine chunk summaries into final output
    combined = "\n\n".join(chunk_summaries)
    return _summarize_single(combined, style)


def _summarize_single(text: str, style: str) -> str:
    """Call Gemini Pro with appropriate prompt based on style."""
    prompts = {
        "comprehensive": f"""You are an expert educator creating comprehensive study notes.
Analyze this video transcript and create well-structured study notes that include:
1. Main Topic and Overview (2-3 sentences)
2. Key Concepts (bullet points with brief explanations)
3. Important Details and Examples (organized by topic)
4. Critical Insights (what makes this content unique or important)
5. Summary (3-4 sentences capturing the essence)
6. Potential Exam/Interview Questions (5 questions a student might be asked)

Transcript:
{text}

Study Notes:""",
        "brief": f"""Summarize the key points from this transcript in 3-5 bullet points.
Be concise but capture all important information.

Transcript:
{text}

Key Points:""",
        "technical": f"""You are a technical expert creating documentation.
From this transcript, extract and organize:
1. Technical Concepts (with definitions)
2. Algorithms or Methods mentioned
3. Tools and Technologies
4. Implementation Details
5. Best Practices mentioned
6. Code or Formulas (if any)

Transcript:
{text}

Technical Notes:""",
        "interview_prep": f"""Create interview preparation material from this transcript:
1. Core Concepts to Know
2. Likely Interview Questions (with brief answers)
3. Key Terms and Definitions
4. Common Mistakes to Avoid (based on content)
5. Quick Reference Summary

Transcript:
{text}

Interview Prep Notes:""",
    }

    prompt = prompts.get(style, prompts["comprehensive"])
    response = model.generate_content(prompt)
    return response.text


def extract_key_topics(transcript: str) -> list:
    """Extract main topics from transcript for tagging."""
    prompt = f"""Extract 5-8 main topics/keywords from this transcript.
Return only a comma-separated list of topics, nothing else.

Transcript:
{transcript[:3000]}

Topics:"""

    response = model.generate_content(prompt)
    topics = [t.strip() for t in response.text.split(",")]
    return topics