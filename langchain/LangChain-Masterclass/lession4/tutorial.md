**Almost every component in LangChain can be treated as a Runnable.**
A Runnable essentially says:
"Give me some input, and I'll produce some output."

**The Runnable Interface**
A Runnable generally supports operations such as:
- invoke() for for one input,
- batch() for multiple inputs,
- stream() for for streaming output.

There are also asynchronous versions such as:
- ainvoke()
- abatch()
- astream()

**RunnableSequence**: When you write: ```chain = prompt | llm | parser```
LangChain creates a sequence of operations.

Conceptually:
     RunnableSequence
       ┌──────────────────────┐
       │                      │
Input → Prompt → LLM → Parser  → Output
       │                      │
       └──────────────────────┘

**A Simple Runnable Sequence**

**RunnableLambda**
Note: In this example you will see that LCEL is not limited to LLMs.
```
from langchain_core.runnables import RunnableLambda
step1 = RunnableLambda(lambda x: x.upper())
step2 = RunnableLambda(lambda x: f"Message: {x}")
chain = step1 | step2
result = chain.invoke("hello langchain")
print(result)
```

RunnableLambda allows you to turn a normal Python function into a Runnable.

```
def double(x: int) -> int:
    return x * 2

from langchain_core.runnables import RunnableLambda
double_runnable = RunnableLambda(double)
result = double_runnable.invoke(5)
print(result)

chain = double_runnable | RunnableLambda(lambda x: x + 5)
print(chain.invoke(10))
```

Why Is This Useful? Suppose you have an AI pipeline.

             User Question
                  ↓
            Clean Input
                  ↓
            Retrieve Documents
                  ↓
            Build Prompt
                  ↓
                 LLM
                  ↓
            Parse Answer
                  ↓
            Save Result

Some steps are LLM operations and others are ordinary Python functions. LCEL allows you to combine them.


**RunnablePassthrough**: It simply returns whatever it receives.
```
from langchain_core.runnables import RunnablePassthrough
passthrough = RunnablePassthrough()
print(passthrough.invoke("Hello"))
```
output: Hello


# RunnablePassthrough Example
data = {"question":"What is Python?"}
 
We want to create
{
    "question": "What is Python?",
    "length": 16
}

```
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough
# 1. Import RunnableParallel
from langchain_core.runnables import RunnableParallel

# 2. Wrap your dictionary structure
chain = RunnableParallel({
    "question": RunnablePassthrough(),
    "length": RunnableLambda(
        lambda x: len(x["question"])
    )
})

# Now .invoke() will work perfectly
result = chain.invoke(
    {
        "question": "What is Python?"
    }
)
print(result)
```

                    ┌→ question → original input
Input Dictionary ───┤
                    └→ length → Python function

**RunnableParallel**: Suppose we want to perform two operations independently. LangChain provides RunnableParallel.


             Input
            /     \
           /       \
     Calculate    Transform
         ↓            ↓
      Result A     Result B

```
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel
)

parallel = RunnableParallel(
    uppercase=RunnableLambda(
        lambda x: x.upper()
    ),

    length=RunnableLambda(
        lambda x: len(x)
    )
)

result = parallel.invoke("LangChain")

print(result)
```

**Parallel AI Processing**: Now let's use two LLM prompts. Imagine we want to analyze a customer complaint 
in two different ways:

                  Customer Complaint
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
       Sentiment Analysis      Category Analysis
              ↓                     ↓
           Positive/Negative      Billing/Technical
              └──────────┬──────────┘
                         ↓
                       Result
```
# 1. Create two chains

sentiment_prompt = ChatPromptTemplate.from_template(
    """
    Analyze the sentiment of this customer message.

    Message:
    {message}

    Return only:
    positive, negative, or neutral.
    """
)

category_prompt = ChatPromptTemplate.from_template(
    """
    Categorize this customer message.

    Message:
    {message}

    Return one category:
    billing, technical, shipping, or other.
    """
)

# 2. Now combine them in a RunnableParallel
analysis = RunnableParallel(
    sentiment=sentiment_chain,
    category=category_chain
)

# 3. invoke
result = analysis.invoke(
    {
        "message":
        "My package is two weeks late and nobody is helping me!"
    }
)

print(result)

```

**RunnableParallel + Prompt**: You can also use RunnableParallel with prompts. In this example, 
we will analyze a customer complaint in two different ways: sentiment analysis and category analysis.

Customer Message
       │
       ├── Sentiment
       │
       ├── Category
       │
       └── Summary

Create a third chain:
```
summary_prompt = ChatPromptTemplate.from_template(
    """
    Summarize this customer complaint in one sentence:

    {message}
    """
)

summary_chain = (
    summary_prompt
    | llm
    | StrOutputParser()
)
analysis = RunnableParallel(
    sentiment=sentiment_chain,
    category=category_chain,
    summary=summary_chain
)
result = analysis.invoke(
    {
        "message":
        "My package is two weeks late and nobody is helping me!"
    }
)
```
This is already starting to look like a real AI application.

**RunnableBranch**: 
Now suppose we want to route questions differently.

For example:

                  Question
                     │
           ┌─────────┴─────────┐
           ↓                   ↓
       Technical?          General?
           ↓                   ↓
   Technical Expert      General Assistant

That's a conditional workflow.

LangChain provides: **RunnableBranch**

```
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables import RunnableLambda

technical = RunnableLambda(
    lambda x: "This looks like a technical question."
)

general = RunnableLambda(
    lambda x: "This looks like a general question."
)

router = RunnableBranch(
    (
        lambda x: "python" in x.lower(),
        technical
    ),
    general
)

print(
    router.invoke(
        "How do I install Python?"
    )
)

```
**RunnableBranch + LLM**
```
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain import StrOutputParser

technical_prompt = ChatPromptTemplate.from_template(
    """
    You are a senior software engineer.

    Answer this technical question:

    {question}
    """
)

general_prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful general assistant.

    Answer this question:

    {question}
    """
)

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)

technical_chain = (
    technical_prompt
    | llm
    | StrOutputParser()
)

general_chain = (
    general_prompt
    | llm
    | StrOutputParser()
)

router = RunnableBranch(
    (
        lambda x:
        any(
            word in x["question"].lower()
            for word in [
                "python",
                "java",
                "docker",
                "kubernetes",
                "api"
            ]
        ),

        technical_chain
    ),
    general_chain
)

result = router.invoke(
    {
        "question":
        "How does Kubernetes work?"
    }
)

print(result)
```

| Concept                  | Purpose                                                                                           | Example                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Runnable**             | A standardized LangChain component that accepts input and produces output.                        | `chain.invoke(input)`                           |
| **RunnableSequence**     | Executes multiple Runnables sequentially.                                                         | `prompt \| llm \| parser`                       |
| **RunnableLambda**       | Converts a normal Python function into a Runnable.                                                | `RunnableLambda(my_function)`                   |
| **RunnablePassthrough**  | Passes the input through unchanged. Useful when constructing input dictionaries.                  | `RunnablePassthrough()`                         |
| **RunnableParallel**     | Executes multiple Runnable branches from the same input and combines their results.               | `RunnableParallel(a=chain_a, b=chain_b)`        |
| **RunnableBranch**       | Routes input to different chains based on a condition.                                            | `RunnableBranch((condition, chain_a), chain_b)` |
| **LCEL (`\|`)**          | Allows Runnables to be composed into readable pipelines.                                          | `prompt \| llm \| parser`                       |
| **`invoke()`**           | Executes a Runnable for a single input.                                                           | `chain.invoke(data)`                            |
| **`batch()`**            | Executes a Runnable against multiple inputs.                                                      | `chain.batch([input1, input2])`                 |
| **`stream()`**           | Streams output incrementally instead of waiting for the complete result.                          | `chain.stream(input)`                           |
| **Sequential Pipeline**  | Passes the output of one component into the next.                                                 | `Prompt → LLM → Parser`                         |
| **Parallel Pipeline**    | Performs multiple independent operations from the same input.                                     | `Message → Sentiment + Category + Summary`      |
| **Conditional Pipeline** | Selects a processing path based on the input.                                                     | `Question → Technical / General`                |
| **Composable Workflows** | Allows Python functions, prompts, LLMs, parsers, retrievers, and other components to be combined. | `cleaner \| prompt \| llm \| parser`            |
