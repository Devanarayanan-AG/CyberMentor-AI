from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq_client import (
    ask_groq,
    generate_quiz,
    generate_interview,
    generate_roadmap
)

from security import detect_prompt_injection


app = FastAPI(
    title="CyberMentor AI",
    version="1.0.0"
)

# Allow Gradio frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


####################################################
# Request Models
####################################################

class TutorRequest(BaseModel):
    question: str
    level: str


class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    questions: int


class InterviewRequest(BaseModel):
    role: str


class RoadmapRequest(BaseModel):
    goal: str
    level: str


####################################################
# Home
####################################################

@app.get("/")
def home():
    return {
        "status": "running",
        "application": "CyberMentor AI",
        "version": "1.0.0"
    }


####################################################
# AI Tutor
####################################################

@app.post("/tutor")
def tutor(data: TutorRequest):

    if detect_prompt_injection(data.question):
        raise HTTPException(
            status_code=400,
            detail="Prompt injection attempt detected."
        )

    try:

        answer = ask_groq(
            question=data.question,
            level=data.level
        )

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


####################################################
# Adaptive Quiz
####################################################

@app.post("/quiz")
def quiz(data: QuizRequest):

    try:

        quiz_json = generate_quiz(

            topic=data.topic,

            difficulty=data.difficulty,

            number_of_questions=data.questions

        )

        return {

            "quiz": quiz_json

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


####################################################
# Interview Preparation
####################################################

@app.post("/interview")
def interview(data: InterviewRequest):

    try:

        response = generate_interview(

            role=data.role

        )

        return {

            "response": response

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


####################################################
# Learning Roadmap
####################################################

@app.post("/roadmap")
def roadmap(data: RoadmapRequest):

    try:

        roadmap = generate_roadmap(

            goal=data.goal,

            level=data.level

        )

        return {

            "roadmap": roadmap

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
