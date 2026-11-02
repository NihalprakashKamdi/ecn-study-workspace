from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openai import OpenAI, OpenAIError

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ecn-tutor")

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
SYSTEM_PROMPT = """You are Circuit, an excellent and patient tutor for MSBTE Diploma Electrical Engineering, ECN 313332 K-Scheme, Unit I: Single Phase AC Series Circuits. Teach from first principles because the learner may be a beginner. Use clear English, correct electrical notation and SI units. Explain every numerical step, state the formula before substitution, keep intermediate values, show units, and check whether the answer is reasonable. For phasor diagrams, explain the reference phasor and the direction of each voltage/current vector. Cover AC generation, sinusoidal quantities, RMS and average values, R/L/C phase relationships, series RL/RC/RLC circuits, impedance, power triangle, power factor, series resonance, resonant frequency and Q-factor. Do not invent syllabus claims. Distinguish a simplified teaching convention from a physical fact when needed. If the learner asks for a question, generate a new exam-style practice problem and do not reveal its solution until asked, unless they explicitly request a solved example. Encourage the learner to attempt a step, but never withhold an explanation when they ask for one. Format responses with short headings and readable equations."""

app = FastAPI(title="ECN Circuit Tutor", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)

class TutorRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=24)

class QuestionRequest(BaseModel):
    topic: str = Field(default="Mixed Unit I", max_length=100)
    difficulty: Literal["Basic", "Intermediate", "Exam level"] = "Intermediate"
    question_type: Literal["Numerical", "Theory", "Mixed"] = "Mixed"


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI is not configured yet. Add a NEW API key to the .env file and restart the app."
        )
    return OpenAI(api_key=api_key)

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "ai_configured": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        "model": MODEL,
        "app": "ECN Circuit Tutor",
    }

@app.post("/api/tutor")
def tutor(request: TutorRequest):
    client = get_client()
    # Keep a bounded context window; no conversation is saved to disk by this app.
    conversation = [{"role": m.role, "content": m.content} for m in request.messages[-18:]]
    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=conversation,
            max_output_tokens=1200,
        )
        answer = (response.output_text or "").strip()
        if not answer:
            raise HTTPException(status_code=502, detail="The model returned an empty answer. Try again.")
        return {"answer": answer, "model": MODEL}
    except OpenAIError as exc:
        logger.exception("OpenAI request failed")
        raise HTTPException(status_code=502, detail="The AI request failed. Check the API key, API billing, model access and internet connection. Server log has the technical error.") from exc

@app.post("/api/question")
def generate_question(request: QuestionRequest):
    client = get_client()
    prompt = (
        f"Create ONE original MSBTE ECN 313332 Unit I practice question. Topic: {request.topic}. "
        f"Difficulty: {request.difficulty}. Type: {request.question_type}. "
        "Return exactly these sections: QUESTION, GIVEN DATA (if numerical), WHAT TO FIND, HINT. "
        "Do not include the final answer or full solution. Ensure values are physically and mathematically sensible. "
        "For a numerical, avoid ambiguous units and provide enough data."
    )
    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt,
            max_output_tokens=650,
        )
        question = (response.output_text or "").strip()
        if not question:
            raise HTTPException(status_code=502, detail="The model returned an empty question. Try again.")
        return {"question": question, "model": MODEL}
    except OpenAIError as exc:
        logger.exception("OpenAI question generation failed")
        raise HTTPException(status_code=502, detail="Question generation failed. Check the API key, API billing, model access and internet connection.") from exc
