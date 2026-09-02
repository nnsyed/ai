import json
import os

def save_note(filename: str, content: str) -> str:
    """Save text content to a local file."""
    try:
        # Simple security check to keep files in the local directory
        clean_filename = os.path.basename(filename)
        with open(clean_filename, "w", encoding="utf-8") as f:
            f.write(content)
        return json.dumps({"status": "success", "message": f"Saved to {clean_filename}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Agent Tool Definition
save_note_tool = {
    "type": "function",
    "function": {
        "name": "save_note",
        "description": "Saves structured text, summaries, or notes into a local file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file (e.g., 'meeting_notes.txt')."
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write inside the file."
                }
            },
            "required": ["filename", "content"]
        }
    }
}
