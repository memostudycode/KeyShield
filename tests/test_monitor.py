"""Unit tests for the monitor module."""

import tempfile
from pathlib import Path

from app.monitor import check_file_for_secrets, is_risky_command, SecretFinding

BODY = "A1b2C3d4E5f6G7h8I9j0KlMn"  # 24 chars, clearly fake


def test_check_file_with_secrets():
    """Test that a file containing secrets is detected."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(f"API_KEY = 'sk-{BODY}'")
        f.flush()
        temp_path = f.name

    try:
        secrets = check_file_for_secrets(temp_path)
        assert len(secrets) == 1
        assert secrets[0].provider == "openai"
        assert secrets[0].masked_value == "sk-****"
        assert secrets[0].file_path == temp_path
    finally:
        Path(temp_path).unlink()


def test_check_file_without_secrets():
    """Test that a file without secrets returns empty list."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("print('hello world')")
        f.flush()
        temp_path = f.name

    try:
        secrets = check_file_for_secrets(temp_path)
        assert len(secrets) == 0
    finally:
        Path(temp_path).unlink()


def test_check_file_with_multiple_providers():
    """Test detection of multiple provider keys in one file."""
    content = f"""
OPENAI_KEY = 'sk-{BODY}'
ANTHROPIC_KEY = 'sk-ant-{BODY}'
GOOGLE_KEY = 'AIza{BODY}'
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(content)
        f.flush()
        temp_path = f.name

    try:
        secrets = check_file_for_secrets(temp_path)
        assert len(secrets) == 3
        providers = {s.provider for s in secrets}
        assert "openai" in providers
        assert "anthropic" in providers
        assert "google" in providers
    finally:
        Path(temp_path).unlink()


def test_check_binary_file():
    """Test that binary files are handled gracefully."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".bin", delete=False) as f:
        f.write(b"\x00\x01\x02\x03")
        f.flush()
        temp_path = f.name

    try:
        secrets = check_file_for_secrets(temp_path)
        assert len(secrets) == 0
    finally:
        Path(temp_path).unlink()


def test_is_risky_command():
    """Test detection of risky commands."""
    assert is_risky_command("git push origin main")
    assert is_risky_command("git upload-pack")
    assert is_risky_command("scp file.txt user@host:/path")
    assert is_risky_command("rsync -av src/ dest/")
    assert is_risky_command("curl -X POST https://api.example.com")
    assert is_risky_command("wget https://example.com/file")


def test_is_risky_command_negative():
    """Test that safe commands are not flagged."""
    assert not is_risky_command("git status")
    assert not is_risky_command("git add .")
    assert not is_risky_command("git commit -m 'test'")
    assert not is_risky_command("python script.py")
    assert not is_risky_command("npm install")


def test_secret_finding_dataclass():
    """Test SecretFinding dataclass."""
    finding = SecretFinding(
        file_path="/path/to/file.py",
        provider="openai",
        masked_value="sk-****",
        line_number=10,
    )
    assert finding.file_path == "/path/to/file.py"
    assert finding.provider == "openai"
    assert finding.masked_value == "sk-****"
    assert finding.line_number == 10


def test_secret_finding_without_line():
    """Test SecretFinding without line number."""
    finding = SecretFinding(
        file_path="/path/to/file.py",
        provider="google",
        masked_value="AIza****",
    )
    assert finding.line_number is None
