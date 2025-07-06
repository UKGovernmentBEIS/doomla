from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import (
    create_agentic_eval_dataset,
    replay_tool_calls,
    set_flags,
    submit_flag,
)


@task
def doomla():
    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "test_multi_flag"})
        ),
        solver=[
            replay_tool_calls(),
            set_flags(),
            react(tools=[bash(), submit_flag()]),
        ],
        scorer=includes(),
    )


eval(doomla, message_limit=6)
