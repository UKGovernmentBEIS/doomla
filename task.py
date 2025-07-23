from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash, python
from inspect_cyber import create_agentic_eval_dataset


@task
def doomla():
    return Task(
        dataset=(
            create_agentic_eval_dataset(root_dir=Path("evals/doomla").resolve())
            # .filter_by_metadata({"variant_name": "solution"})
        ),
        solver=react(tools=[bash(), python()]),
        scorer=includes(),
    )


eval(doomla, model="anthropic/claude-sonnet-4-20250514", token_limit=5_000)
