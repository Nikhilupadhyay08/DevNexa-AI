from pathlib import Path

from app.agents.tools import create_patch_tool, run_linter_tool


def test_create_patch_tool():
    target_file = Path("tests/patch_target.py")
    original_content = 'PATCH_TARGET_VALUE = "before"\n'

    target_file.write_text(
        original_content,
        encoding="utf-8",
    )

    try:
        result = create_patch_tool(
            file_path="tests/patch_target.py",
            old_content='PATCH_TARGET_VALUE = "before"',
            new_content='PATCH_TARGET_VALUE = "after"',
        )

        assert result["file_path"] == "tests/patch_target.py"
        assert result["changed"] is True
        assert "--- tests/patch_target.py" in result["diff"]
        assert "+++ tests/patch_target.py" in result["diff"]
        assert '-PATCH_TARGET_VALUE = "before"' in result["diff"]
        assert '+PATCH_TARGET_VALUE = "after"' in result["diff"]

        actual_content = target_file.read_text(encoding="utf-8")

        assert actual_content == original_content

    finally:
        if target_file.exists():
            target_file.unlink()


def test_run_linter_tool():
    target_file = Path("tests/linter_target.py")

    target_file.write_text(
        'message = "hello"\nprint(message)\n',
        encoding="utf-8",
    )

    try:
        result = run_linter_tool("tests/linter_target.py")

        assert result["target"] == "tests/linter_target.py"
        assert result["command"].startswith("ruff check")
        assert result["exit_code"] == 0
        assert result["success"] is True

    finally:
        if target_file.exists():
            target_file.unlink()