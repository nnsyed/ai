import json
from openai import OpenAI
from config import (OPENAI_MODEL,api_key)
from tools import (TOOLS, execute_tool)

client = OpenAI(api_key=api_key)
SYSTEM_INSTRUCTIONS = """
You are an Enterprise Employee Assistant.
You have access to:
1. Oracle employee data
2. Compensation calculation tools
3. Public REST APIs

The Oracle SCOTT EMP.SAL column represents MONTHLY salary.

When answering questions about employees:
- Use Oracle tools rather than inventing data.
- Use tools whenever database information is required.
- Do not invent employees or salaries.
- When calculating compensation, use the
  compensation calculator.
- When converting currencies, obtain the
  exchange rate using the REST API.
- Clearly distinguish monthly salary from
  annual compensation.

For compensation:
Annual base salary =
new monthly salary * 12

Percentage bonus =
new monthly salary * bonus percentage

Total annual compensation =
annual base salary + bonus

Explain calculations clearly.

Never claim that an external API was called
unless the tool actually returned a result.
"""
def run_agent(user_question,conversation):
    conversation.append({
        "role": "user",
        "content": user_question
    })

    # ======================================================
    # Initial request
    # ======================================================
    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=conversation,
        tools=TOOLS
    )

    # ======================================================
    # Agent loop
    # ======================================================
    while True:
        tool_outputs = []
        for item in response.output:
            # ------------------------------------------------
            # Ignore normal text
            # ------------------------------------------------
            if item.type != "function_call":
                continue
            print(f"\n[TOOL] {item.name}")
            print(f"[ARGS] {item.arguments}")

            try:
                arguments = json.loads(item.arguments)

                # --------------------------------------------
                # Execute Python tool
                # --------------------------------------------
                result = execute_tool(item.name,arguments)
                print(f"[RESULT] {result}")
                tool_outputs.append({
                    "type":"function_call_output",
                    "call_id":item.call_id,
                    "output":json.dumps(result)
                })
            except Exception as e:
                print(f"[ERROR] Tool failed: {e}")
                tool_outputs.append({
                    "type":"function_call_output",
                    "call_id":item.call_id,
                    "output":
                        json.dumps({
                            "success": False,
                            "error": str(e)
                        })
                })

        # ==================================================
        # No tool requested
        # ==================================================
        if not tool_outputs:
            answer = response.output_text
            conversation.append({
                "role": "assistant",
                "content": answer
            })
            return answer

        # ==================================================
        # Send tool results back to GPT
        # ==================================================
        response = client.responses.create(
            model=OPENAI_MODEL,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS
        )

# ==========================================================
# Chat application
# ==========================================================
def main():
    conversation = []
    print("==========================================")
    print(" Oracle Employee AI Assistant")
    print("==========================================")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ")

        if question.lower() in {"exit","quit"}:
            break
        try:
            answer = run_agent(question,conversation)
            print("\nAI:",answer)
        except Exception as e:
            print("\nERROR:",e)
if __name__ == "__main__":
    main()

