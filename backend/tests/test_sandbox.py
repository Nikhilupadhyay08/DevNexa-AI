from sandbox.sandbox import run_in_sandbox


def test_run_in_sandbox():
    result = run_in_sandbox(
        ["-c", "print(2 + 3)"],
    )

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert result["stdout"] == "5\n"
    assert result["stderr"] == ""