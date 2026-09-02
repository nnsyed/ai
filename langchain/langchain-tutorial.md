# LangChain: A Complete Overview & Tutorial

## Before you start: a note on languages

LangChain is officially a **Python and JavaScript/TypeScript** framework. There is no official Java build. The closest Java equivalent is **[LangChain4j](https://docs.langchain4j.dev/)**, an independent community project that borrows LangChain's concepts (chains, agents, retrievers, memory) but has its own API and its own maintainers — it is not a port of LangChain's code. This tutorial covers real, working **Python LangChain** for every concept, and pairs each one with the equivalent in **LangChain4j** so you have a working Java path too. Just don't expect method-for-method parity between the two.

---

## 1. What LangChain actually is

LangChain is a framework for building applications powered by LLMs. The core problem it solves: an LLM API call in isolation is just "text in, text out." Real applications need the model to use tools, remember prior turns, pull in outside data, follow multi-step plans, and produce structured output. LangChain gives you standardized building blocks for all of that so you're not reinventing them per-project.

The ecosystem has a few separate packages (Python):

| Package | Purpose |
|---|---|
| `langchain-core` | Base abstractions: messages, prompts, runnables, output parsers |
| `langchain` | Chains, agents, retrieval logic built on core |
| `langchain-openai`, `langchain-anthropic`, etc. | Provider-specific model integrations |
| `langgraph` | Graph-based orchestration for stateful, multi-step agents (the modern way to build agents) |
| `langsmith` | Observability/tracing/eval platform (separate paid product, optional) |

**Core concepts you'll use in nearly every app:**

1. **Chat Models** — the LLM wrapper (`ChatOpenAI`, `ChatAnthropic`, etc.)
2. **Prompts / Prompt Templates** — reusable, parameterized prompts
3. **Runnables & LCEL (LangChain Expression Language)** — the `|` pipe syntax for composing steps
4. **Output Parsers** — turning raw model output into structured Python objects
5. **Memory** — carrying conversation state across turns
6. **Retrieval (RAG)** — embeddings, vector stores, retrievers for grounding answers in your own data
7. **Tools & Agents** — letting the model call functions/APIs and decide what to do next
8. **LangGraph** — building agents as explicit state graphs (replaces older `AgentExecutor` patterns)

Install:

```bash
pip install langchain langchain-openai langchain-community langgraph langchain-chroma
```

Set your API key:

```bash
export OPENAI_API_KEY="sk-..."
```

---

## 2. Chat Models — the basics

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

response = model.invoke("Explain what a vector database is in two sentences.")
print(response.content)
```

`invoke()` is the universal method across LangChain — every component you build (model, prompt, chain, retriever) exposes `invoke`, `stream`, and `batch`. Learn that trio once and it applies everywhere.

```python
# Streaming
for chunk in model.stream("Write a haiku about databases."):
    print(chunk.content, end="", flush=True)

# Batch (parallel calls)
results = model.batch(["What is Python?", "What is Java?"])
```

### Messages

Conversations are lists of typed messages:

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="You are a terse, expert Python tutor."),
    HumanMessage(content="What's a generator?"),
]
response = model.invoke(messages)
print(response.content)
```

---

## 3. Prompt Templates

Templates let you parameterize prompts instead of string-formatting by hand.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{text}"),
])

formatted = prompt.invoke({
    "input_language": "English",
    "output_language": "French",
    "text": "I love programming.",
})
print(formatted.to_messages())
```

---

## 4. LCEL — composing pipelines with `|`

This is LangChain's signature pattern. Any `Runnable` can be piped into the next:

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "input_language": "English",
    "output_language": "Spanish",
    "text": "Where is the nearest train station?",
})
print(result)  # "¿Dónde está la estación de tren más cercana?"
```

Each stage: `dict → ChatPromptValue → AIMessage → str`. Because everything is a `Runnable`, you get `.stream()`, `.batch()`, and async (`.ainvoke()`) for free on the whole chain, not just the model.

### Parallel branches with `RunnableParallel`

```python
from langchain_core.runnables import RunnableParallel

summary_chain = ChatPromptTemplate.from_template("Summarize: {text}") | model | StrOutputParser()
sentiment_chain = ChatPromptTemplate.from_template("What's the sentiment (positive/negative/neutral) of: {text}") | model | StrOutputParser()

combined = RunnableParallel(summary=summary_chain, sentiment=sentiment_chain)
print(combined.invoke({"text": "The product arrived late but support was fantastic."}))
# {'summary': '...', 'sentiment': '...'}
```

---

## 5. Structured Output

Instead of parsing free text, ask the model to return a typed object directly.

```python
from pydantic import BaseModel, Field

class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating out of 10")
    summary: str = Field(description="One-sentence summary")

structured_model = model.with_structured_output(MovieReview)

result = structured_model.invoke("Review the movie Inception in a structured way.")
print(result.title, result.rating, result.summary)
```

`with_structured_output` uses the provider's native tool-calling/JSON mode under the hood, so it's reliable — no manual regex parsing of markdown-fenced JSON.

---

## 6. Memory (conversation state)

Modern LangChain handles memory by threading message history explicitly rather than a magic `Memory` object (older `ConversationBufferMemory` classes are legacy). The clean way is `RunnableWithMessageHistory`:

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{history}"),
    ("human", "{input}"),
])

chain = prompt | model
chat_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user-123"}}

chat_with_memory.invoke({"input": "My name is Priya."}, config=config)
response = chat_with_memory.invoke({"input": "What's my name?"}, config=config)
print(response.content)  # "Your name is Priya."
```

(If you use `langgraph`, its built-in checkpointer is now the more common way to persist conversation state — see section 9.)

---

## 7. Retrieval-Augmented Generation (RAG)

RAG grounds the model in your own documents: embed text into vectors, store them, retrieve the most relevant chunks for a query, and stuff them into the prompt.

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough

# 1. Load
loader = TextLoader("company_handbook.txt")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 3. Embed + store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 4. Build the RAG chain
rag_prompt = ChatPromptTemplate.from_template(
    "Answer the question using only the context below.\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | model
    | StrOutputParser()
)

print(rag_chain.invoke("How many vacation days do employees get?"))
```

This pattern — retriever feeds `context`, the raw question passes through — is the standard RAG shape you'll see everywhere in LangChain code.

---

## 8. Tools & Tool Calling

Tools let the model call real functions.

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # pretend this hits a real API
    return f"It's 22°C and sunny in {city}."

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

tools = [get_weather, multiply]
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke("What's the weather in Tokyo, and what's 12 times 7?")
for call in response.tool_calls:
    print(call["name"], call["args"])
```

The model returns *requests* to call tools — you execute them and feed results back:

```python
messages = [HumanMessage(content="What's the weather in Tokyo?")]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

for call in ai_msg.tool_calls:
    selected_tool = {"get_weather": get_weather, "multiply": multiply}[call["name"]]
    tool_result = selected_tool.invoke(call["args"])
    messages.append(ToolMessage(content=str(tool_result), tool_call_id=call["id"]))

final = model_with_tools.invoke(messages)
print(final.content)
```

(Import `ToolMessage` from `langchain_core.messages`.)

---

## 9. Agents with LangGraph

The old `AgentExecutor` API is legacy; **LangGraph** is now the recommended way to build agents — it models the agent as an explicit graph of nodes (model call, tool call, etc.) with control over loops and state. For the common "ReAct-style" tool-using agent, there's a prebuilt constructor:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools)

result = agent.invoke({
    "messages": [HumanMessage(content="What's the weather in Tokyo, then multiply that temperature by 3.")]
})
for m in result["messages"]:
    m.pretty_print()
```

For custom control flow, you build the graph yourself:

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

graph_builder = StateGraph(MessagesState)

def call_model(state: MessagesState):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()

result = graph.invoke({"messages": [HumanMessage(content="What's 15 times the temperature in Tokyo?")]})
result["messages"][-1].pretty_print()
```

This is the pattern worth internalizing: **state → node functions → conditional edges → compiled graph**. It scales from simple tool agents to complex multi-agent systems.

---

## 10. Putting it together: a small RAG chatbot with memory

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatOpenAI(model="gpt-4o-mini")
docs = TextLoader("docs.txt").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
retriever = Chroma.from_documents(chunks, OpenAIEmbeddings()).as_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using this context:\n{context}"),
    ("placeholder", "{history}"),
    ("human", "{input}"),
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

base_chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["input"])))
    | prompt
    | model
    | StrOutputParser()
)

store = {}
def get_history(session_id):
    return store.setdefault(session_id, InMemoryChatMessageHistory())

chatbot = RunnableWithMessageHistory(
    base_chain, get_history, input_messages_key="input", history_messages_key="history"
)

config = {"configurable": {"session_id": "demo"}}
print(chatbot.invoke({"input": "What does the doc say about refunds?"}, config=config))
print(chatbot.invoke({"input": "And what about the timeframe for that?"}, config=config))
```

---

## 11. The Java side: LangChain4j

LangChain4j mirrors these ideas with its own idiomatic Java API (builders, interfaces, annotations). Maven dependency:

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>0.36.2</version>
</dependency>
```

### Basic chat model call

```java
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.chat.ChatLanguageModel;

ChatLanguageModel model = OpenAiChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName("gpt-4o-mini")
        .build();

String answer = model.generate("Explain what a vector database is in two sentences.");
System.out.println(answer);
```

### Prompt templates

```java
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import java.util.Map;

PromptTemplate template = PromptTemplate.from(
    "You are a helpful assistant that translates {{input_language}} to {{output_language}}.\n{{text}}"
);

Prompt prompt = template.apply(Map.of(
    "input_language", "English",
    "output_language", "French",
    "text", "I love programming."
));

String result = model.generate(prompt.text());
System.out.println(result);
```

### Structured output (AI Services)

LangChain4j's signature feature is **AI Services** — declare a Java interface, get an LLM-backed implementation:

```java
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.SystemMessage;

interface MovieReviewer {
    @SystemMessage("You review movies concisely and return the fields requested.")
    MovieReview review(String movieTitle);
}

record MovieReview(String title, int rating, String summary) {}

MovieReviewer reviewer = AiServices.create(MovieReviewer.class, model);
MovieReview result = reviewer.review("Inception");
System.out.println(result.rating());
```

### Memory

```java
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.service.AiServices;

interface Assistant {
    String chat(String userMessage);
}

Assistant assistant = AiServices.builder(Assistant.class)
        .chatLanguageModel(model)
        .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
        .build();

System.out.println(assistant.chat("My name is Priya."));
System.out.println(assistant.chat("What's my name?"));  // "Your name is Priya."
```

### RAG (retrieval)

```java
import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.model.embedding.onnx.allminilml6v2.AllMiniLmL6V2EmbeddingModel;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.rag.content.retriever.EmbeddingStoreContentRetriever;

Document document = FileSystemDocumentLoader.loadDocument("company_handbook.txt");

InMemoryEmbeddingStore<dev.langchain4j.data.segment.TextSegment> store = new InMemoryEmbeddingStore<>();
var embeddingModel = new AllMiniLmL6V2EmbeddingModel();

EmbeddingStoreIngestor.builder()
        .documentSplitter(DocumentSplitters.recursive(500, 50))
        .embeddingModel(embeddingModel)
        .embeddingStore(store)
        .build()
        .ingest(document);

var retriever = EmbeddingStoreContentRetriever.builder()
        .embeddingStore(store)
        .embeddingModel(embeddingModel)
        .maxResults(4)
        .build();

interface RagAssistant {
    String answer(String question);
}

RagAssistant ragAssistant = AiServices.builder(RagAssistant.class)
        .chatLanguageModel(model)
        .contentRetriever(retriever)
        .build();

System.out.println(ragAssistant.answer("How many vacation days do employees get?"));
```

### Tools

```java
import dev.langchain4j.agent.tool.Tool;

class WeatherTools {
    @Tool("Get the current weather for a city")
    String getWeather(String city) {
        return "It's 22°C and sunny in " + city + ".";
    }
}

interface WeatherAssistant {
    String chat(String message);
}

WeatherAssistant weatherAssistant = AiServices.builder(WeatherAssistant.class)
        .chatLanguageModel(model)
        .tools(new WeatherTools())
        .build();

System.out.println(weatherAssistant.chat("What's the weather in Tokyo?"));
```

---

## 12. Python vs. LangChain4j — conceptual map

| Concept | Python LangChain | LangChain4j |
|---|---|---|
| Model wrapper | `ChatOpenAI(...)` | `OpenAiChatModel.builder()...build()` |
| Composition | LCEL `|` pipes, `Runnable` | Manual chaining, or `AiServices` interfaces |
| Structured output | `model.with_structured_output(PydanticModel)` | `AiServices` interface return type |
| Memory | `RunnableWithMessageHistory` / LangGraph checkpointer | `ChatMemory` (e.g. `MessageWindowChatMemory`) |
| Tools | `@tool` decorator + `bind_tools` | `@Tool` annotation + `AiServices.tools(...)` |
| Agents | LangGraph (`create_react_agent`, custom `StateGraph`) | `AiServices` with tools (simpler, less graph-based) |
| RAG | Document loaders → splitter → vector store → retriever | Same pipeline, different class names |

---

## 13. Practical tips

- **Prefer LCEL and LangGraph over legacy classes.** `LLMChain`, `ConversationChain`, and `AgentExecutor` still work but are considered legacy; new LangChain code and docs are built around LCEL runnables and LangGraph.
- **Pin your versions.** LangChain moves fast and has broken changes between minor versions historically — pin `langchain`, `langchain-core`, and provider packages together.
- **Use LangSmith (optional) for debugging.** Once chains get more than 2–3 steps, tracing (`LANGCHAIN_TRACING_V2=true`) saves enormous debugging time versus print-statements.
- **Chunk size matters more than people expect in RAG.** Start around 500–1000 characters with 10–20% overlap, then tune based on retrieval quality, not guesswork.
- **Structured output > prompt-engineered JSON.** Always prefer `with_structured_output` (Python) or typed `AiServices` interfaces (Java) over asking the model to "return JSON" in a plain prompt — the native tool-calling path is far more reliable.

---

*Note: I don't have live access to a package registry or the LangChain docs site while writing this, so double-check exact class names and current version numbers (e.g. `langchain-chroma`, LangChain4j version) against the official docs at python.langchain.com and docs.langchain4j.dev before shipping — APIs in this space evolve quickly.*
