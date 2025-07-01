from inspect_ai.tool import Tool, tool


@tool
def check_flag(correct_flags: list[str]) -> Tool:
    async def execute(guessed_flag: str):
        """
        Check whether or not a flag is correct.

        Args:
            guessed_flag (str): The flag to check.

        Returns:
            out (str): "correct", "incorrect", or "no flag provided".
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
