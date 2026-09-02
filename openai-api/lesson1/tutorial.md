
**Lesson 1 — Build Your First OpenAI Terminal Chatbot**


Simple api call:
              ┌─────────────┐
              │     User    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │     LLM     │
              └──────┬──────┘
                     │
                     ▼
                  Answer


Chatbot:

                 Terminal
                    │
                    │
              "What is Python?"
                    │
                    ▼
             ┌──────────────┐
             │   Python     │
             │  chatbot.py  │
             └──────┬───────┘
                    │
                    │ API Request
                    ▼
             ┌──────────────┐
             │   OpenAI     │
             │    Model     │
             └──────┬───────┘
                    │
                    │ Response
                    ▼
             ┌──────────────┐
             │   Python     │
             │  chatbot.py  │
             └──────┬───────┘
                    │
                    ▼
                 Terminal

**Understand the Response**
response
│
├── id
├── model
├── status
├── output
│
├── usage
│   ├── input_tokens
│   ├── output_tokens
│   └── total_tokens
│
└── other metadata

| Concept              | What you learned                  |
| -------------------- | --------------------------------- |
| `OpenAI()`           | Creates the API client            |
| `responses.create()` | Sends a request to the model      |
| `model`              | Selects the model                 |
| `input`              | Sends the user's request          |
| `response`           | Complete API response object      |
| `output_text`        | Extracts generated text           |
| `usage`              | Token consumption information     |
| Environment variable | Secure API-key configuration      |
| Terminal loop        | Turns one API call into a chatbot |

The most important takeaway:
---------------------------
the OpenAI API is fundamentally just a request/response mechanism. 
Everything that makes an application an Agent—memory, tools, planning, 
retrieval, loops, etc.—gets built around this fundamental interaction.