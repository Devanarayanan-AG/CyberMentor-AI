import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CyberMentorEngine:
    def __init__(self):
        self.client = Groq()

    def generate_stream(self, system_prompt: str, message: str, history: list):
        """Handles the core streaming infrastructure via Groq's high-speed API."""
        messages = [{"role": "system", "content": system_prompt}]
        
        # FIXED FOR GRADIO 6.0: Iterating through ChatMessage objects/dictionaries natively
        for msg in history:
            # Handle both object attributes or dictionary keys safely
            role = getattr(msg, 'role', None) or msg.get('role')
            content = getattr(msg, 'content', None) or msg.get('content')
            if role and content:
                messages.append({"role": role, "content": content})
                
        # Append the new message from the user
        messages.append({"role": "user", "content": message})
        
        try:
            # Updated to the fully supported Llama 3.1 model identifier
            response_stream = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=2548,
                stream=True
            )
            partial_message = ""
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    partial_message += chunk.choices[0].delta.content
                    yield partial_message
        except Exception as e:
            yield f"⚠️ Engine Error: {str(e)}"

    def tutor_chat(self, message: str, history: list, difficulty: str):
        system_prompt = (
            f"You are the Tutor mode of CyberMentor AI. Teach concepts strictly at a '{difficulty}' skill level.\n"
            "Break down topics with bold markdown structural elements. Provide concrete, real-world examples "
            "and always conclude your response with a quick, interactive practice drill to challenge the user."
        )
        yield from self.generate_stream(system_prompt, message, history)

    def quiz_chat(self, message: str, history: list, topic: str, difficulty: str, num_questions: int):
        system_prompt = (
            f"You are the Adaptive AI Quiz mode of CyberMentor AI.\n"
            f"Target Assessment Parameter: Topic='{topic}', Difficulty='{difficulty}', Total Questions={num_questions}.\n"
            "When the user types 'Start Quiz', generate multiple-choice questions with 4 options (A, B, C, D).\n"
            "Present exactly one question at a time. Wait for their answer turn, evaluate it instantly with a comprehensive "
            "explanation, and then seamlessly serve the next question.\n"
            "At the final question, deliver a detailed Scorecard, Performance Analysis, Weakness Breakdown, and "
            "targeted learning recommendations."
        )
        yield from self.generate_stream(system_prompt, message, history)

    def interview_chat(self, message: str, history: list, role: str):
        system_prompt = (
            f"You are a Mock Technical Interviewer for the role of '{role}'.\n"
            "Conduct a highly professional, interactive mock interview. Ask technical, role-specific interview questions "
            "one by one. Wait for the user's answer, provide a critical review along with a scorecard metrics rating (e.g., [8/10]), "
            "then proceed to ask the next realistic technical question."
        )
        yield from self.generate_stream(system_prompt, message, history)
