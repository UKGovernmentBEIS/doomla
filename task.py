"""Entry point for running the doomla evaluation."""

import os
from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import create_agentic_eval_dataset

# Default to a mock model so the evaluation runs out of the box without an API
# key. Set INSPECT_EVAL_MODEL (e.g. in a .env file) to use a real model.
DEFAULT_MODEL = "mockllm/model"


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


eval(doomla, model=os.environ.get("INSPECT_EVAL_MODEL", DEFAULT_MODEL))
