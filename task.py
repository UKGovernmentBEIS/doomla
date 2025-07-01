from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import create_agentic_eval_dataset, replay_tool_calls


@task
def doomla():
    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "joomla_version"})
        ),
        solver=[replay_tool_calls(), react(tools=[bash()])],
        scorer=includes(),
    )


eval(doomla, message_limit=15)
