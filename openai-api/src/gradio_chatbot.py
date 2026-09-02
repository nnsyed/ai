'''
                 User
                  │
                  ▼
      Gradio Textbox (Input)
                  │
                  ▼
         ask_chatgpt(user_input)
                  │
                  ▼
     Responses API
     ├── instructions = SYSTEM_PROMPT
     └── input = user_input
                  │
                  ▼
            GPT-5 Model
                  │
                  ▼
        response.output_text
                  │
                  ▼
      Gradio Textbox (Output)
'''
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define a system prompt
SYSTEM_PROMPT = """
You are a friendly Python tutor.

Rules:
- Explain concepts simply.
- Use beginner-friendly examples.
- Keep answers under 150 words.
"""

# Function called when user clicks Submit
def ask_chatgpt(user_input):

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=user_input
    )

    return response.output_text


# Create Gradio UI
demo = gr.Interface(
    fn=ask_chatgpt,
    inputs=gr.Textbox(
        label="Ask a Python Question",
        placeholder="Example: What is a list in Python?"
    ),
    outputs=gr.Textbox(label="AI Response"),
    title="Python Tutor",
    description="Ask any Python question."
)

demo.launch()