"""
E2E Demo Script: YouTube Transcript → Gemini Question Generator
Run this from the /backend folder:

  python demo_e2e.py

Reads GEMINI_API_KEY from the .env file in this directory automatically.
"""
import asyncio
import os
import json

# Load .env BEFORE importing our app modules
from dotenv import load_dotenv
load_dotenv()  # Reads backend/.env automatically

# Add the backend root to sys.path so our app modules are importable
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.adapters.youtube_adapter import YoutubeTranscriptAdapter
from app.infrastructure.adapters.gemini_adapter import GeminiAdapter
from app.domain.schemas import QuestionGenerationContext


# --- CONFIGURATION (set these in your .env file) ---
# Paste the YouTube Video ID here (the part after ?v= in the URL)
# Example: https://www.youtube.com/watch?v=CV_Uf3Dq-EU → ID is "CV_Uf3Dq-EU"
VIDEO_ID = os.getenv("VIDEO_ID", "CV_Uf3Dq-EU")
TRANSCRIPT_CHUNK_MAX_CHARS = 1500  # Limit chunk size to keep costs low


async def main():
    print("\n" + "="*60)
    print("  [TubeRPG] -- E2E Demo")
    print("="*60)

    if not os.getenv("GEMINI_API_KEY"):
        print("\n[ERROR] GEMINI_API_KEY is not set in your .env file.")
        return

    # Step 1: Fetch real YouTube transcript
    print(f"\n[1/3] Fetching transcript for video ID: {VIDEO_ID}")
    youtube = YoutubeTranscriptAdapter()
    transcript = youtube.get_transcript(VIDEO_ID)
    chunk = transcript[:TRANSCRIPT_CHUNK_MAX_CHARS]
    print(f"[OK] Got {len(transcript)} chars. Using first {len(chunk)} chars as the chunk.\n")
    print("--- Transcript Chunk Preview ---")
    print(chunk[:300] + "...")
    print("--------------------------------\n")

    # Step 2: Call Gemini to generate a question
    print("[2/3] Calling Gemini to generate a battle question...")
    context = QuestionGenerationContext(
        video_id=VIDEO_ID,
        transcript_chunk=chunk,
        player_level=1,
        topic_focus="Tech/Programming"
    )

    gemini = GeminiAdapter()
    question = await gemini.generate_question(context)

    # Step 3: Print the result
    print("\n[3/3] Question Generated!\n")
    print(">>> BATTLE QUESTION:")
    print(f"    {question.question_text}\n")
    for opt in question.options:
        marker = "  [CORRECT]" if opt.id == question.correct_option_id else "          "
        print(f"{marker} [{opt.id}] {opt.text}")
    print(f"\n[Explanation]: {question.explanation}")
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
