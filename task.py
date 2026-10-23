"""Entry point for running the doomla evaluation."""

from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import create_agentic_eval_dataset


@task
def doomla():
    """Build the doomla task, which runs the `solution` dataset variant."""
    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "solution"})
        ),
        solver=react(tools=[bash()]),
        scorer=includes(),
    )


eval(doomla)
