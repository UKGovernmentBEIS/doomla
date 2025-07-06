import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Callable, Iterable

from inspect_ai import Task, eval, task
from inspect_ai.agent import AgentAttempts, AgentSubmit, react
from inspect_ai.dataset import Sample
from inspect_ai.tool import bash, python
from inspect_cyber import (
    create_agentic_eval_dataset,
    multi_flag_scorer,
    replay_tool_calls,
    set_flags,
    submit_flag,
)


def split_solution_script_by_milestone() -> Callable[[Sample], Iterable[Sample]]:
    def _split_solution_script_by_milestone(sample: Sample) -> list[Sample]:
        # For each "MILESTONE" in the solution script, create one sample that contains a setup script of the solution script up to the line with that "MILESTONE"

        samples = []

        solution_script_path = (
            Path(__file__).parent / "evals" / "doomla" / "solution" / "solution.sh"
        )
        with open(solution_script_path, "r") as f:
            solution_script_lines = f.readlines()

        milestone_indices = []
        for i, line in enumerate(solution_script_lines):
            if line.startswith("# MILESTONE"):
                milestone_indices.append(i)

        temp_dir = Path(tempfile.mkdtemp(prefix="milestone_setup_scripts"))

        for i, milestone_idx in enumerate(milestone_indices):
            setup_script_lines = [
                line for line in solution_script_lines[:milestone_idx]
                if not line.startswith("# MILESTONE")
            ]

            temp_setup_path = temp_dir / f"setup_milestone_{i}.sh"
            with open(temp_setup_path, "w") as f:
                f.writelines(setup_script_lines)

            variant = deepcopy(sample)
            variant.id = f"{sample.metadata.get("eval_name")} (milestone {i})"
            variant.files = {**sample.files, "setup.sh": str(temp_setup_path)}
            variant.metadata.update({"milestone": i})

            samples.append(variant)

        return samples

    return _split_solution_script_by_milestone


@task
def doomla():
    tools = [bash(), python()]
    return Task(
        dataset=(
            create_agentic_eval_dataset(root_dir=Path("evals/doomla").resolve())
            .filter_by_metadata({"variant_name": "conditional_success"})
            .flat_map(mapper=split_solution_script_by_milestone())
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
        scorer=multi_flag_scorer(),
    )


eval(doomla, message_limit=15)
