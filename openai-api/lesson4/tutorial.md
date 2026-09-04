**Structured Outputs**
Instead of asking the LLM to return a paragraph, we can ask it to return data that conforms to a schema.

Text based question to LLM:
Analyze this customer review:
"The food was excellent but the service was very slow."

Text based Response back from LLM:
The customer had a mixed experience. They liked
the food but were unhappy with the slow service.

Intead if recieve something like this:
```json
{
    "sentiment": "mixed",
    "rating": 3,
    "positive_aspects": [
        "food"
    ],
    "negative_aspects": [
        "service"
    ]
}
```

**What is Schema?**
A schema is a structured format that defines the expected structure and types of data. 
In the context of the OpenAI API, a schema can be used to guide the LLM in generating 
structured output that conforms to a specific format.

We can represent it using Pydantic models. Pydantic is a data validation and settings 
management library for Python, which allows us to define data models with type annotations.

pip install pydantic




                    OPENAI API
                        │
                        ▼
              ┌─────────────────┐
              │      LLM        │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      Text        Conversation     Structured
     Response        Memory          Output
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                  Python App


What we have learned

| Concept             | Meaning                           |
| ------------------- | --------------------------------- |
| Structured Output   | Model returns predictable data    |
| Schema              | Defines expected structure        |
| Pydantic            | Python schema/model definition    |
| `BaseModel`         | Defines structured data           |
| `responses.parse()` | Requests parsed structured output |
| `text_format`       | Specifies expected schema         |
| `output_parsed`     | Access parsed result              |
| `Literal`           | Restricts allowed values          |
| Application logic   | Python can act on model output    |
