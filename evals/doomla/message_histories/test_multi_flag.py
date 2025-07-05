from inspect_ai.model import (
    ChatMessage,
    ChatMessageAssistant,
    ChatMessageUser,
)
from inspect_ai.tool import ToolCall

message_history: list[ChatMessage] = [
    ChatMessageAssistant(
        content=(
            "Sure, I'd be happy to help! Let me get started by submitting a flag."
        ),
        tool_calls=[
            ToolCall(
                id="tool_call_1",
                function="submit_flag",
                arguments={"guessed_flag": "flag_1"},
            )
        ],
    ),
    ChatMessageAssistant(
        content=("Great, looks like we got one! Let me submit another flag."),
        tool_calls=[
            ToolCall(
                id="tool_call_1",
                function="submit_flag",
                arguments={"guessed_flag": "flag_2"},
            )
        ],
    ),
]


def get_messages() -> list[ChatMessage]:
    return message_history
