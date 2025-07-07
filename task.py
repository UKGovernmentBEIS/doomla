from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import AgentAttempts, AgentSubmit, react
from inspect_ai.tool import bash, python
from inspect_cyber import (
    captured_flags,
    create_agentic_eval_dataset,
    replay_tool_calls,
    set_flags,
    split_solution_script_by_milestone,
    submit_flag,
)


@task
def doomla():
    tools = [bash(), python()]
    return Task(
        dataset=(
            create_agentic_eval_dataset(root_dir=Path("evals/doomla").resolve())
            .filter_by_metadata({"variant_name": "conditional_success"})
            .flat_map(
                mapper=split_solution_script_by_milestone(
                    solution_script_path=Path("evals/doomla/solution/solution.sh")
                )
            )
        ),
        solver=[
            set_flags(),
            replay_tool_calls(tools + [submit_flag()]),
            react(
                tools=tools,
                submit=AgentSubmit(
                    name="submit_flag", description="Submit a flag.", tool=submit_flag()
                ),
                attempts=AgentAttempts(
                    attempts=2**10,
                    incorrect_message="You can do this! Keep trying!",
                ),
            ),
        ],
        scorer=captured_flags(),
    )


eval(doomla, message_limit=15)
