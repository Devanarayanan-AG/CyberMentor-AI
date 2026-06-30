import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"


##############################
# API CALLS
##############################

def tutor(question, level):

    if question.strip() == "":
        return "Please enter a question."

    try:

        response = requests.post(

            API_URL + "/tutor",

            jsons={

                "question": question,

                "level": level

            }

        )

        return response.json()["answer"]

    except:

        return "Backend is not running."


##############################

def generate_quiz(topic, difficulty, questions):

    try:

        response = requests.post(

            API_URL + "/quiz",

            json={

                "topic": topic,

                "difficulty": difficulty,

                "questions": questions

            }

        )

        return response.json()["quiz"]

    except:

        return "Unable to connect to backend."


##############################

def interview(role):

    try:

        response = requests.post(

            API_URL + "/interview",

            params={

                "role": role

            }

        )

        return response.json()["response"]

    except:

        return "Unable to connect to backend."


##############################

def roadmap(goal, level):

    try:

        response = requests.post(

            API_URL + "/roadmap",

            params={

                "goal": goal,

                "level": level

            }

        )

        return response.json()["roadmap"]

    except:

        return "Unable to connect to backend."


#######################################################

with gr.Blocks(

        title="CyberMentor AI",

        theme=gr.themes.Soft(

            primary_hue="blue",

            secondary_hue="cyan"

        )

) as demo:

    gr.Markdown(

        """

# 🛡 CyberMentor AI

### AI Powered Cybersecurity Learning Platform

"""

    )

    ##########################################################

    with gr.Tab("🤖 AI Tutor"):

        gr.Markdown("### Learn Cybersecurity with AI")

        level = gr.Radio(

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ],

            value="Beginner",

            label="Difficulty"

        )

        question = gr.Textbox(

            lines=5,

            label="Ask your question"

        )

        answer = gr.Markdown()

        ask = gr.Button(

            "Ask AI",

            variant="primary"

        )

        ask.click(

            tutor,

            inputs=[

                question,

                level

            ],

            outputs=answer

        )

    ##########################################################

    with gr.Tab("📝 Adaptive Quiz"):

        gr.Markdown("### AI Generated Quiz")

        topic = gr.Dropdown(

            [

                "Networking",

                "Linux",

                "Python",

                "Cryptography",

                "OWASP Top 10",

                "SIEM",

                "Threat Hunting",

                "Incident Response",

                "Cloud Security",

                "Digital Forensics",

                "Malware Analysis"

            ],

            value="Networking",

            label="Topic"

        )

        difficulty = gr.Radio(

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ],

            value="Beginner",

            label="Difficulty"

        )

        number = gr.Slider(

            minimum=5,

            maximum=20,

            value=5,

            step=5,

            label="Number of Questions"

        )

        quiz_button = gr.Button(

            "Generate Quiz",

            variant="primary"

        )

        quiz = gr.Markdown()

        quiz_button.click(

            generate_quiz,

            inputs=[

                topic,

                difficulty,

                number

            ],

            outputs=quiz

        )

    ##########################################################

    with gr.Tab("🎤 Interview Preparation"):

        role = gr.Dropdown(

            [

                "SOC Analyst",

                "Penetration Tester",

                "Blue Team",

                "Red Team",

                "Threat Hunter",

                "Cloud Security Engineer",

                "Incident Responder"

            ],

            value="SOC Analyst",

            label="Target Job Role"

        )

        interview_button = gr.Button(

            "Start Interview",

            variant="primary"

        )

        interview_output = gr.Markdown()

        interview_button.click(

            interview,

            inputs=role,

            outputs=interview_output

        )

    ##########################################################

    with gr.Tab("🗺 Learning Roadmap"):

        goal = gr.Textbox(

            label="Career Goal",

            placeholder="Become a SOC Analyst"

        )

        level2 = gr.Radio(

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ],

            value="Beginner",

            label="Current Skill"

        )

        roadmap_button = gr.Button(

            "Generate Roadmap",

            variant="primary"

        )

        roadmap_output = gr.Markdown()

        roadmap_button.click(

            roadmap,

            inputs=[

                goal,

                level2

            ],

            outputs=roadmap_output

        )

    ##########################################################

    with gr.Tab("📊 Progress Dashboard"):

        gr.Markdown("""

### Progress Analytics

Coming Soon

✔ Quiz History

✔ Weak Areas

✔ Strong Areas

✔ Learning Graph

✔ Recommendations

✔ Performance Trend

""")

############################################################

demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)
