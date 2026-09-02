**Lesson 2 - Prompt Templates, Messages, Output Parsers, and LCEL**
By the end of this lesson, you'll understand the four core concepts that almost every LangChain application uses:

✅ ChatPromptTemplate
✅ SystemMessage, HumanMessage, and AIMessage
✅ StrOutputParser
✅ LCEL (prompt | model | parser)

We'll build this pipeline:
User Input
     │
     ▼
Prompt Template
     │
     ▼
Chat Model
     │
     ▼
Output Parser
     │
     ▼
  String


**What is a Prompt Template?**
Suppose you repeatedly write prompts like this:
```
f"""
Explain {topic}
using simple language
in {language}
"""
```
Imagine you do this in 40 different places. Maintenance becomes difficult.
Instead we create a template. Think of it like a mail merge document.

```
Hello {name}
Welcome to {company}
```
Later we replace the variables.

Hello John
Welcome to OpenAI

Creating a Prompt Template

```
prompt = ChatPromptTemplate.from_template(
    """
    Explain {topic} in simple English.
    Limit the explanation to {lines} lines.
    """
)
```

**Messages**
Every chat conversation is composed of messages.

    System
      ↓
    Human
      ↓
      AI
      ↓
    Human
      ↓
      AI

LangChain models these explicitly.
There are three primary message types.

**HumanMessage**: Represents the user's input.
```
from langchain_core.messages import HumanMessage
msg = HumanMessage(
    content="Explain Docker")
print(msg)
```


**AIMessage**: Represents the model's reply.
```
response = llm.invoke("Hello")
print(type(response))
```

**SystemMessage**: This is arguably the most important message type. It tells the AI how to behave.

Example: You are a Python professor.
Instead of a single template string, we can build a prompt from multiple message roles.

```prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert Python instructor."),
        ("human", "Explain {topic}")
    ])
```
Invoke it:
```
prompt_value = prompt.invoke(
    {
        "topic": "Decorators"
    }
)
print(prompt_value)
```

**Parsers**: LangChain provides output parsers.
Response is AIMessage, not a string. To convert it to a string, we can use an output parser.

```
parser = StrOutputParser()
text = parser.invoke(response)
print(text)
```

**Output parsers can be String, JSON, or even a custom parser (pydantic objects).**

**LCEL (LangChain Expression Language)**
This is one of LangChain's most elegant ideas. Instead of manually invoking each component:
```
prompt_value = prompt.invoke(data)
response = llm.invoke(prompt_value)
answer = parser.invoke(response)
```
we compose them into a pipeline.

**chain = prompt | llm | parser**

```
llm = ChatOpenAI(model="gpt-4.1-mini", 
                 api_key = os.getenv("OPENAI_API_KEY"),
                 temperature=0.7, 
                 max_tokens=500)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert Python instructor."),
        ("human", "Explain {topic} in {lines} lines")
    ])
parser = StrOutputParser()
chain = prompt | llm | parser
answer = chain.invoke({"topic": "lamda functions", "lines": 6})
```

LangChain effectively performs these steps:
Variables
      │
      ▼
ChatPromptTemplate
      │
      ▼
ChatPromptValue (messages)
      │
      ▼
ChatOpenAI
      │
      ▼
AIMessage
      │
      ▼
StrOutputParser
      │
      ▼
   String


┌─────────────────────────────────────────────────────────────────────────────────────┐
| **Concept**                      | **Purpose**                                      |
| -------------------------------- | ------------------------------------------------ |
| **ChatPromptTemplate**           | Creates reusable prompts with variables.         |
| **SystemMessage**                | Defines the assistant's role and behavior.       |
| **HumanMessage**                 | Represents the user's request.                   |
| **AIMessage**                    | Represents the model's response.                 |
| **StrOutputParser**              | Converts an `AIMessage` into a plain string.     |
| **LCEL**(prompt | llm | parser)  | Composes reusable processing pipelines.          |
| **chain.invoke()**               | Executes the entire pipeline with a single call. |
└─────────────────────────────────────────────────────────────────────────────────────┘