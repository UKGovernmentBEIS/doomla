import re
from pathlib import Path

from inspect_ai import Task, eval, task
from inspect_ai.agent import react
from inspect_ai.scorer import includes
from inspect_ai.tool import bash
from inspect_cyber import create_agentic_eval_dataset, replay_tool_calls

idxs = [
    "PUBLIC_NET",
    "WEB_IP",
    "JOOMLA_VERSION",
    "PASSWORD",
]


@task
def doomla(start_idx: int, end_idx: int):
    start_value = idxs[start_idx]

    # Create setup.sh which contains everything in solution.sh before start_value
    solution_path = (
        Path(__file__).parent / "evals" / "doomla" / "solution" / "solution.sh"
    )
    with open(solution_path, "r") as solution_file:
        solution_lines = solution_file.readlines()

    setup_lines = []
    for line in solution_lines:
        if re.search(
            rf"echo.*\b{re.escape(start_value)}\b|{re.escape(start_value)}.*echo", line
        ):
            break
        setup_lines.append(line)

    # Ensure target directory exists
    setup_path = Path("evals/doomla/setup.sh")
    setup_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the setup script
    with open(setup_path, "w") as setup_file:
        setup_file.writelines(setup_lines)

    return Task(
        dataset=(
            create_agentic_eval_dataset(
                root_dir=Path("evals/doomla").resolve()
            ).filter_by_metadata({"variant_name": "conditional_progress"})
        ),
        solver=[replay_tool_calls(), react(tools=[bash()])],
        scorer=includes(),
    )


eval(doomla(start_idx=1), message_limit=15)
