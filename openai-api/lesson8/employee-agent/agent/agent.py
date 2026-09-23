import json
import logging
from openai import OpenAI
from config import OPENAI_MODEL
from agent.prompts import SYSTEM_PROMPT
from tools.registry import (TOOL_DEFINITIONS, execute_tool)

logger = logging.getLogger(__name__)

class EmployeeAgent:
    def __init__(self):
        self.client = OpenAI()
        self.previous_response_id = None

    # ======================================================
    # Ask agent
    # ======================================================
    def ask(self, question):
        logger.info("User question: %s", question)

        response = self.client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=question,
            tools=TOOL_DEFINITIONS,
            previous_response_id=
                self.previous_response_id
                if self.previous_response_id
                else None
        )

        # Remember response
        self.previous_response_id=(response.id)
        # ==================================================
        # Agent loop
        # ==================================================
        while True:
            tool_outputs = []
            for item in response.output:
                if item.type != "function_call":
                    continue
                logger.info("Tool requested: %s", item.name)

                try:
                    arguments = json.loads(item.arguments)
                    logger.info("Tool arguments: %s",arguments)
                    result = execute_tool(item.name, arguments)
                    logger.info("Tool result: %s", result)
                    tool_outputs.append({
                        "type":"function_call_output",
                        "call_id":item.call_id,
                        "output":json.dumps(result)
                    })
                except Exception as exc:
                    logger.exception("Tool execution failed")
                    tool_outputs.append({
                        "type":"function_call_output",
                        "call_id":item.call_id,
                        "output":
                            json.dumps({
                                "success":False,
                                "error":str(exc)
                            })
                    })

            # ==================================================
            # Finished
            # ==================================================
            if not tool_outputs:
                return response.output_text

            # ==================================================
            # Continue agent
            # ==================================================
            response = self.client.responses.create(
                model=OPENAI_MODEL,
                instructions=SYSTEM_PROMPT,
                input=tool_outputs,
                tools=TOOL_DEFINITIONS,
                previous_response_id=
                    response.id
            )
            self.previous_response_id = (response.id)