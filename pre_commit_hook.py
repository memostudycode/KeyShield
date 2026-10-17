#!/usr/bin/env python3
"""Git pre-commit hook for KeyShield.

This script is installed as a git pre-commit hook to block commits that
contain exposed API keys. It scans all staged files and aborts the commit
if secrets are detected.

To install: cp pre_commit_hook.py .git/hooks/pre-commit
Make it executable: chmod +x .git/hooks/pre-commit
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# Add the working-tree root to the path so the hook can import app modules.
try:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
except OSError as exc:
    print(f"[KeyShield] Could not locate the Git repository: {exc}", file=sys.stderr)
    sys.exit(1)

if result.returncode != 0 or not result.stdout.strip():
    detail = result.stderr.strip() or "Git did not return a repository root."
    print(f"[KeyShield] Could not locate the Git repository: {detail}", file=sys.stderr)
    sys.exit(1)

project_root = result.stdout.strip()
sys.path.insert(0, project_root)

from app.detector import scan

def show_desktop_popup(file_path: str, provider: str, masked_value: str) -> None:
    """Display native Windows desktop warning popup using tkinter."""
    try:
        # Create a Python script to show the popup
        popup_script = f"""
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()
message = (
    f"Git commit blocked!\\n\\n"
    f"File: {file_path}\\n"
    f"Provider: {provider}\\n"
    f"Masked Secret: {masked_value}\\n\\n"
    f"Please remove the secret before committing."
)
messagebox.showwarning(
    title="KeyShield Pre-Commit Alert",
    message=message,
    parent=root
)
root.destroy()
"""
        # Run the popup script in a separate process
        subprocess.Popen(
            [sys.executable, "-c", popup_script],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
    except Exception as e:
        print(f"[Popup Error] Could not show desktop popup: {e}", file=sys.stderr)


def check_file_for_secrets(file_path: str) -> list[dict]:
    """Scan a single file for API secrets.

    Returns list of dicts with secret details.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return []

    masked_text, findings = scan(content)

    if not findings:
        return []

    results = []
    for finding in findings:
        results.append({
            "file_path": file_path,
            "provider": finding.type,
            "masked_value": finding.masked,
            "start": finding.start,
            "end": finding.end,
        })

    return results


def main() -> int:
    """Main pre-commit hook function.

    Returns 0 to allow commit, 1 to block commit.
    """
    # Get list of staged files
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            # Not a git repo or no staged files, allow commit
            return 0

        staged_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        if not staged_files:
            return 0

    except (subprocess.SubprocessError, FileNotFoundError):
        return 0

    # Check each staged file for secrets
    all_secrets = []
    affected_files = set()

    for file_path in staged_files:
        full_path = os.path.join(os.getcwd(), file_path)
        if os.path.isfile(full_path):
            secrets = check_file_for_secrets(full_path)
            if secrets:
                all_secrets.extend(secrets)
                affected_files.add(file_path)

    # If secrets found, block commit and show warnings
    if all_secrets:
        print("\n" + "=" * 70, file=sys.stderr)
        print("KEYSHIELD PRE-COMMIT HOOK", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print(f"\nCOMMIT BLOCKED: Secrets detected in {len(affected_files)} file(s)\n", file=sys.stderr)

        print("AFFECTED FILES:", file=sys.stderr)
        for file_path in affected_files:
            print(f"  - {file_path}", file=sys.stderr)

        print("\nSECRETS DETECTED:", file=sys.stderr)
        for secret in all_secrets:
            print(f"  - {secret['provider']}: {secret['masked_value']} in {secret['file_path']}", file=sys.stderr)

        print("\nACTION REQUIRED:", file=sys.stderr)
        print("  1. Remove or mask the secrets in the affected files")
        print("  2. Stage the fixed files again")
        print("  3. Retry the commit")
        print("\n" + "=" * 70 + "\n", file=sys.stderr)

        # Show desktop popup for each secret
        for secret in all_secrets:
            show_desktop_popup(
                file_path=secret['file_path'],
                provider=secret['provider'],
                masked_value=secret['masked_value']
            )

        # Block the commit
        return 1

    # No secrets found, allow commit
    return 0


if __name__ == "__main__":
    sys.exit(main())
