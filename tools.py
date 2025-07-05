from inspect_ai.tool import Tool, tool
from inspect_ai.util import StoreModel
from pydantic import Field


class FlagSubmissions(StoreModel):
    correct_flags: list[str] = Field(default_factory=list)
    flag_submissions: int = Field(default=0)
    flags_submitted: dict[str, int] = Field(default_factory=dict)  # Counter
    flags_found: list[str] = Field(default_factory=list)


@tool
def submit_flag(correct_flags: list[str]) -> Tool:
    async def execute(guessed_flag: str):
        """
        Submit a flag.

        Args:
            guessed_flag (str): The submitted flag.

        Returns:
            out (str): Message corresponding to whether or not the flag is correct.
        """
        if guessed_flag is None:
            return "No flag was provided."
        if guessed_flag in correct_flags:
            # TODO: increment metadata.flags_found iff it's a new flag found
            # TODO: do we want to require the agent submit the flags in a certain order?
            # To access TaskState, will need to use Store
            return (
                "Well done! That is a correct flag! You now have X flags. Only Y flags "
                "left to find."
            )
        else:
            return "That is not a correct flag."

    return execute
