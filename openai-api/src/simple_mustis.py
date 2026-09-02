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
You are the best tourist guide the Bay Area and you are going to help me tour different places in the Bay Area. 
You will provide me with information about the places, including their history, significance, and any 
interesting facts. You will also provide me with recommendations for things to do and see in the area. 
You will be friendly, informative, and engaging in your responses.
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
        label="Hello Customer!! How may I help you!!!",
        placeholder="Example: I can make your travel easy?"
    ),
    outputs=gr.Textbox(label="AI Response"),
    title="Agent's Assistant",
    description="Ask any question."
)

demo.launch()