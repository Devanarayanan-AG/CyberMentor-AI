import gradio as gr
from cyber_engine import CyberMentorEngine

engine = CyberMentorEngine()

# --- HELPER WRAPPERS FOR GRADIO 6.0 CHATMESSAGE COMPLIANCE ---
def tutor_wrapper(message, history, difficulty):
    for text_response in engine.tutor_chat(message, history, difficulty):
        yield gr.ChatMessage(role="assistant", content=text_response)

def quiz_wrapper(message, history, topic, difficulty, num_questions):
    for text_response in engine.quiz_chat(message, history, topic, difficulty, num_questions):
        yield gr.ChatMessage(role="assistant", content=text_response)

def interview_wrapper(message, history, role):
    for text_response in engine.interview_chat(message, history, role):
        yield gr.ChatMessage(role="assistant", content=text_response)


# Custom dark-emerald theme configuration
theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="slate",
    font=[gr.themes.GoogleFont("Source Code Pro"), "ui-monospace", "monospace"]
)

with gr.Blocks(title="CyberMentor AI Platform") as demo:
    gr.Markdown(
        """
        # 🛡️ CyberMentor AI: Cybersecurity Learning Ecosystem
        *An intelligent, multi-modular hub providing personalized tutoring, adaptive testing, and career-readiness mock interviews.*
        """
    )
    
    with gr.Tabs():
        # --- TAB 1: TUTOR ---
        with gr.Tab("🤖 AI Cybersecurity Tutor"):
            gr.Markdown("### Personalized Tutoring & Real-World Concepts")
            with gr.Row():
                tutor_diff = gr.Dropdown(["Beginner", "Intermediate", "Advanced"], value="Beginner", label="Explanation Level")
            
            # FIXED: Removed type="messages" to conform to Gradio 6.0 structure
            tutor_bot = gr.Chatbot(height=450, placeholder="Ask me to explain any cybersecurity concept or mechanism...")
            
            gr.ChatInterface(
                fn=tutor_wrapper,
                chatbot=tutor_bot,
                additional_inputs=[tutor_diff],
                textbox=gr.Textbox(placeholder="Ask Tutor...", container=False)
            )

        # --- TAB 2: ADAPTIVE QUIZ ---
        with gr.Tab("📝 Adaptive AI Quiz"):
            gr.Markdown("### Dynamic Concept Testing & Deep Analytics")
            with gr.Row():
                quiz_topic = gr.Textbox(value="Network Security", label="Cybersecurity Topic")
                quiz_diff = gr.Dropdown(["Beginner", "Intermediate", "Advanced"], value="Intermediate", label="Difficulty Level")
                quiz_num = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="Number of Questions")
            
            # FIXED: Removed type="messages"
            quiz_bot = gr.Chatbot(height=450, placeholder="Type 'Start Quiz' to generate your custom assessment.")
            
            gr.ChatInterface(
                fn=quiz_wrapper,
                chatbot=quiz_bot,
                additional_inputs=[quiz_topic, quiz_diff, quiz_num],
                textbox=gr.Textbox(placeholder="Type 'Start Quiz' or submit your answer...", container=False)
            )

        # --- TAB 3: MOCK INTERVIEW ---
        with gr.Tab("🎤 AI Interview Preparation"):
            gr.Markdown("### Role-Specific Technical Career Drills")
            with gr.Row():
                job_role = gr.Dropdown(
                    ["SOC Analyst", "Penetration Tester", "Threat Hunter", "Incident Responder", "Cloud Security Engineer"],
                    value="SOC Analyst",
                    label="Target Professional Role"
                )
            
            # FIXED: Removed type="messages"
            interview_bot = gr.Chatbot(height=450, placeholder="Type 'Begin Interview' to start your technical mock evaluation session.")
            
            gr.ChatInterface(
                fn=interview_wrapper,
                chatbot=interview_bot,
                additional_inputs=[job_role],
                textbox=gr.Textbox(placeholder="Type 'Begin Interview' or respond to the question...", container=False)
            )

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        share=False,
        theme=theme
    )
