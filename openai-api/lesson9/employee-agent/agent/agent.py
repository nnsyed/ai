'''
STARTING
   │
   ▼
THINKING
   │
   ▼
CALLING_TOOL
   │
   ▼
PROCESSING_TOOL_RESULT
   │
   ▼
THINKING
   │
   ▼
GENERATING
   │
   ▼
COMPLETED

If something goes wrong:

         ┌─────────┐
         │ ERROR   │
         └─────────┘
'''

import json
import logging

from openai import OpenAI
from config import *
from agent.prompts import SYSTEM_PROMPT
from tools.registry import TOOL_DEFINITIONS
from tools.registry import execute_tool

logger = logging.getLogger(__name__)


class EmployeeAgent:
    def __init__(self):
        self.client = OpenAI()
        self.previous_response_id = None

    def emit(self,event_type,message):
        print(f"\n🤖 {message}")

    def ask(self, question):
        self.emit("STARTED","Understanding request...")

        try:
            response = self.client.responses.create(
                model=OPENAI_MODEL,
                instructions=SYSTEM_PROMPT,
                input=question,
                tools=TOOL_DEFINITIONS,
                previous_response_id=(self.previous_response_id),
                stream=False
            )

            while True:
                tool_outputs = []
                for item in response.output:
                    if item.type == "function_call":
                        tool_name = item.name
                        arguments = json.loads(item.arguments)
                        self.emit("TOOL_STARTED",f"Calling {tool_name}...")

                        try:
                            result = execute_tool(tool_name,arguments)
                            print(f"✓ {tool_name} " f"completed")
                        except Exception as exc:
                            print(f"✗ {tool_name} " f"failed: {exc}")
                            result = {"success": False, "error": str(exc) }

                        tool_outputs.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        })

                if not tool_outputs:
                    self.previous_response_id = (response.id)
                    print("\n🤖 Preparing final answer...")
                    return response.output_text
                self.emit("PROCESSING", "Processing tool results...")

                response = (
                    self.client.responses.create(
                        model=OPENAI_MODEL,
                        instructions=SYSTEM_PROMPT,
                        previous_response_id=response.id,
                        input=tool_outputs,
                        tools=TOOL_DEFINITIONS
                    )
                )
        except Exception as exc:
            logger.exception("Agent failed")
            print(f"\n❌ Agent error: {exc}")
            return ("I was unable to complete " "the request.")
