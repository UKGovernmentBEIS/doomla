"""Tasks for running and verifying the Doomla! cyber range."""

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import create_agentic_eval_dataset, verify_solutions


@task
def doomla():
    """Run a real agent against the unsolved challenge. Requires a model.

    Run with: inspect eval task.py@doomla --model anthropic/claude-sonnet-5
    """
    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "example"})
        ),
        solver=react(tools=[bash()]),
        scorer=includes(),
    )


@task
def doomla_solutions():
    """Run the challenge's solution script directly, with no model.

    This is a quick, free sanity check that the range itself (images,
    networking, credentials, etc.) is configured correctly.

    Run with: inspect eval task.py@doomla_solutions
    """
    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "solution"})
        ),
        solver=verify_solutions(),
        scorer=includes(),
    )
