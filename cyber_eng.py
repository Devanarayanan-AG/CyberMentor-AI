import os
import chromadb
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

class CyberMentorEngine:
    def __init__(self):
        self.client = Groq()
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="cybermentor_base")

    def process_user_upload(self, file_obj):
        """Dynamic parser supporting both standard .txt and structural .pdf uploads."""
        if file_obj is None:
            return "⚠️ No file uploaded."
           
        try:
            raw_text = ""
            filename = file_obj.name.lower()
           
            # --- EXTRACTION PIPELINE ---
            if filename.endswith(".pdf"):
                reader = PdfReader(file_obj.name)
                # Loop through all pages in the PDF file and append their text
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        raw_text += text + "\n"
            else:
                # Default text extraction method for .txt files
                with open(file_obj.name, "r", encoding="utf-8") as f:
                    raw_text = f.read()
           
            if not raw_text.strip():
                return "❌ Document Processing Failure: Could not extract readable text."

            # --- VECTOR STORE SYSTEM RESET ---
            try:
                self.chroma_client.delete_collection(name="cybermentor_base")
            except Exception:
                pass
            self.collection = self.chroma_client.get_or_create_collection(name="cybermentor_base")
           
            # --- CHUNKING & INGESTION ---
            chunks = [raw_text[i:i+600] for i in range(0, len(raw_text), 600)]
           
            doc_counter = 0
            for chunk in chunks:
                if chunk.strip():
                    self.collection.add(
                        documents=[chunk],
                        ids=[f"user_id_{doc_counter}"]
                    )
                    doc_counter += 1
                   
            return f"✅ Successfully parsed {doc_counter} chunks from your file! The AI context is now updated."
        except Exception as e:
            return f"❌ Ingestion Error: {str(e)}"

    def _retrieve_context(self, query: str) -> str:
        try:
            results = self.collection.query(query_texts=[query], n_results=2)
            if results and results.get('documents') and results['documents'][0]:
                return "\n".join(results['documents'][0])
        except Exception:
            pass
        return ""

    def generate_stream(self, system_prompt: str, message: str, history: list):
        retrieved_context = self._retrieve_context(message)
       
        augmented_system = system_prompt
        if retrieved_context:
            augmented_system += (
                "\n\n[AUGMENTED KNOWLEDGE BASE CONTEXT]\n"
                "You must heavily ground your answer using this verified institutional data:\n"
                f"{retrieved_context}\n"
                "----------------------------------------"
            )

        messages = [{"role": "system", "content": augmented_system}]
       
        for msg in history:
            role = getattr(msg, 'role', None) or msg.get('role')
            content = getattr(msg, 'content', None) or msg.get('content')
            if role and content:
                messages.append({"role": role, "content": content})
               
        messages.append({"role": "user", "content": message})
       
        try:
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