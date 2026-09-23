from datetime import datetime

class AgentEvent:
    def __init__(self, event_type, message, tool_name=None):
        self.timestamp = datetime.now()
        self.event_type = event_type
        self.message = message
        self.tool_name = tool_name

    def display(self):
        timestamp = (self.timestamp.strftime("%H:%M:%S"))
        if self.tool_name:
            print( f"[{timestamp}] " f"{self.message}: " f"{self.tool_name}")
        else:
            print(f"[{timestamp}] " f"{self.message}")