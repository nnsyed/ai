'''
Question
      │
      ▼
 ChatOpenAI
      │
      ▼
 AIMessage

+-------------------------------------------------------------------------+
| Concept            | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| `ChatOpenAI`       | Connects your application to an OpenAI chat model. |
| `.env`             | Keeps API keys out of your source code.            |
| `load_dotenv()`    | Loads environment variables from the `.env` file.  |
| `invoke()`         | Sends input to the model and receives a response.  |
| `AIMessage`        | The structured object returned by the model.       |
| `response.content` | The generated text from the model.                 |
| Chat loop          | Allows repeated interactions with the model.       |

'''
import re
import token

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from pprint import pprint

# details of the response object
'''
AIMessage
├── content
├── metadata
├── token usage
├── model
└── response information
'''
def inspect_ai_message(message):
    print("=" * 80)
    print("TYPE")
    print("=" * 80)
    print(type(message))

    print("\n" + "=" * 80)
    print("CONTENT")
    print("=" * 80)
    print(message.content)

    print("\n" + "=" * 80)
    print("ID")
    print("=" * 80)
    print(message.id)

    print("\n" + "=" * 80)
    print("USAGE METADATA")
    print("=" * 80)
    pprint(message.usage_metadata)

    print("\n" + "=" * 80)
    print("RESPONSE METADATA")
    print("=" * 80)
    pprint(message.response_metadata)

    print("\n" + "=" * 80)
    print("TOOL CALLS")
    print("=" * 80)
    pprint(message.tool_calls)

    print("\n" + "=" * 80)
    print("ADDITIONAL KWARGS")
    print("=" * 80)
    pprint(message.additional_kwargs)
    usage = message.usage_metadata
    print(f"Input Tokens  : {usage['input_tokens']}")
    print(f"Output Tokens : {usage['output_tokens']}")
    print(f"Total Tokens  : {usage['total_tokens']}")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Please check your .env file."
    )

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=api_key,
    temperature=0.1,
)
print("=" * 60)
print("LangChain Chatbot")
print("Type 'quit' to exit")
print("=" * 60)

while True:
    question = input("\nYou: ")
    #
    # Check if the user wants to quit
    if question.lower() == "quit":
        break

    response = llm.invoke(question)

    # class 'langchain_core.messages.ai.AIMessage'
    print(type(response))
    print("\nAI:", response.content)

inspect_ai_message(response)