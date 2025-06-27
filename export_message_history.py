"""Export message history to JSON for use in eval.yaml."""

import json
from pathlib import Path

from inspect_ai.model import ChatMessage

from message_history import message_history_example

# Directory to save message history files
output_dir = Path("evals/doomla/message_history")
output_dir.mkdir(exist_ok=True, parents=True)

# Export message_history_example
output_file = output_dir / "message_history_example.json"


# Convert message history to JSON
def message_to_dict(message: ChatMessage) -> dict:
    """Convert a ChatMessage to a dictionary."""
    result = message.model_dump()
    # Handle any custom serialization here if needed
    return result


# Export the messages
messages_data = [message_to_dict(msg) for msg in message_history_example.messages]

# Write to file
with open(output_file, "w") as f:
    json.dump(messages_data, f, indent=2)

print(f"Exported message history to {output_file}")
print(
    "Reference in eval.yaml as: message_history: "
    "message_history/message_history_example.json"
)
