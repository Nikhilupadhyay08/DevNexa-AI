import subprocess
from pathlib import Path


SANDBOX_IMAGE = "devnexa-sandbox:latest"
SANDBOX_WORKSPACE = Path(__file__).resolve().parent / "workspace"

ALLOWED_TEST_COMMANDS = {
    "pytest": ["python", "-m", "pytest"],
}


def run_in_sandbox(
    command: list[str],
    timeout: int = 30,
) -> dict:
    if not command:
        raise ValueError("Command cannot be empty")

    if timeout < 1:
        raise ValueError("Timeout must be at least 1 second")

    if timeout > 300:
        raise ValueError("Timeout cannot exceed 300 seconds")

    SANDBOX_WORKSPACE.mkdir(parents=True, exist_ok=True)

    docker_command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--memory",
        "512m",
        "--cpus",
        "1.0",
        "-v",
        f"{SANDBOX_WORKSPACE}:/workspace:ro",
        SANDBOX_IMAGE,
        "python",
        *command,
    ]

    try:
        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"Sandbox execution timed out after {timeout} seconds.",
        }


def run_project_tests(
    test_command: str = "pytest",
    timeout: int = 60,
) -> dict:
    if test_command not in ALLOWED_TEST_COMMANDS:
        raise ValueError(
            f"Unsupported test command: {test_command}"
        )

    command = [
        "-c",
        (
            "import subprocess; "
            "result = subprocess.run("
            "['python', '-m', 'pytest', '-p', 'no:cacheprovider'], "
            "cwd='/workspace', "
            "capture_output=True, "
            "text=True"
            "); "
            "print(result.stdout, end=''); "
            "print(result.stderr, end=''); "
            "raise SystemExit(result.returncode)"
        ),
    ]

    return run_in_sandbox(
        command=command,
        timeout=timeout,
    )