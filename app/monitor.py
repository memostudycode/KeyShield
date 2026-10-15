"""Real-time file operation monitoring for KeyShield.

Watches for risky operations (git push, uploads) that may expose secrets
and displays warnings when API keys are detected in affected files.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.detector import scan

# Import watchdog only when needed (for file watching)
# This allows the module to be imported without watchdog for testing
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

# Risky commands that may expose secrets
RISKY_COMMANDS = ["git push", "git upload", "scp", "rsync", "curl", "wget"]


@dataclass
class SecretFinding:
    """Represents a secret found in a file."""

    file_path: str
    provider: str
    masked_value: str
    line_number: Optional[int] = None


@dataclass
class WarningContext:
    """Context for a warning message."""

    operation: str
    secrets_found: list[SecretFinding]
    affected_files: set[str]


def show_desktop_popup(finding: SecretFinding) -> None:
    """Display native Windows desktop warning popup using tkinter.

    Shows warning title, full file path, secret provider type, and masked secret key.
    Runs in a separate thread to avoid blocking the file monitor.
    """
    def _show_popup():
        try:
            # Create a hidden root window
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            # Build the warning message
            message = (
                f"File: {finding.file_path}\n"
                f"Provider: {finding.provider}\n"
                f"Masked Secret: {finding.masked_value}"
            )

            # Show warning popup
            messagebox.showwarning(
                title="KeyShield Security Alert",
                message=message,
                parent=root
            )

            # Clean up
            root.destroy()
        except Exception as e:
            # If tkinter fails (e.g., no display), fall back to terminal
            print(f"\n[Popup Error] Could not show desktop popup: {e}", file=sys.stderr)
            print(f"Secret detected in {finding.file_path}: {finding.provider} {finding.masked_value}", file=sys.stderr)

    # Run popup in a separate thread (non-daemon to ensure it completes)
    popup_thread = threading.Thread(target=_show_popup, daemon=False)
    popup_thread.start()


def check_file_for_secrets(file_path: str) -> list[SecretFinding]:
    """Scan a single file for API secrets.

    Returns list of SecretFinding objects if secrets are found.
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
        results.append(
            SecretFinding(
                file_path=file_path,
                provider=finding.type,
                masked_value=finding.masked,
            )
        )

    return results


def check_git_staged_files() -> WarningContext | None:
    """Check git staged files for secrets before push.

    Returns WarningContext if secrets are found, None otherwise.
    """
    try:
        # Get list of staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None

        staged_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        if not staged_files:
            return None

        all_secrets = []
        affected_files = set()

        for file_path in staged_files:
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.isfile(full_path):
                secrets = check_file_for_secrets(full_path)
                if secrets:
                    all_secrets.extend(secrets)
                    affected_files.add(file_path)

        if all_secrets:
            return WarningContext(
                operation="git push",
                secrets_found=all_secrets,
                affected_files=affected_files,
            )

    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return None


def display_warning_box(context: WarningContext) -> None:
    """Display a prominent warning box in the terminal."""
    print("\n" + "=" * 70, file=sys.stderr)
    print("KEYSHIELD SECURITY WARNING", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(f"\nRISKY OPERATION DETECTED: {context.operation}", file=sys.stderr)
    print(f"Secret keys found in {len(context.affected_files)} file(s)\n", file=sys.stderr)

    print("AFFECTED FILES:", file=sys.stderr)
    for file_path in context.affected_files:
        print(f"  - {file_path}", file=sys.stderr)

    print("\nSECRETS DETECTED:", file=sys.stderr)
    for secret in context.secrets_found:
        print(f"  - {secret.provider}: {secret.masked_value} in {secret.file_path}", file=sys.stderr)

    print("\nLEAKAGE RISK:", file=sys.stderr)
    print("  These API keys will be exposed if you proceed with this operation.", file=sys.stderr)
    print("  This could lead to unauthorized access to your accounts.")

    print("\nYOUR OPTIONS:", file=sys.stderr)
    print("  1. View secrets - Use KeyShield web UI to see full details")
    print("  2. Auto-mask - Run: keyshield mask <file_path>")
    print("  3. Abort - Cancel the operation manually (Ctrl+C)")
    print("\n" + "=" * 70 + "\n", file=sys.stderr)


def pre_push_hook() -> int:
    """Git pre-push hook to check for secrets.

    Returns 0 to allow push, 1 to block (if configured to block).
    Currently this only warns and always returns 0 (non-blocking).
    """
    context = check_git_staged_files()
    if context:
        display_warning_box(context)
        # Non-blocking: always allow the operation
        return 0
    return 0


def is_risky_command(command_line: str) -> bool:
    """Check if a command line contains risky operations."""
    command_lower = command_line.lower()
    return any(risky in command_lower for risky in RISKY_COMMANDS)


def scan_current_directory() -> WarningContext | None:
    """Scan all files in current directory for secrets.

    Returns WarningContext if secrets are found, None otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None

        tracked_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except (subprocess.SubprocessError, FileNotFoundError):
        # Not a git repo, scan common source files
        tracked_files = []
        for ext in [".py", ".js", ".ts", ".java", ".go", ".rs", ".env", ".json", ".yaml", ".yml"]:
            tracked_files.extend(str(p) for p in Path(".").rglob(f"*{ext}"))

    all_secrets = []
    affected_files = set()

    for file_path in tracked_files:
        if os.path.isfile(file_path):
            secrets = check_file_for_secrets(file_path)
            if secrets:
                all_secrets.extend(secrets)
                affected_files.add(file_path)

    if all_secrets:
        return WarningContext(
            operation="directory scan",
            secrets_found=all_secrets,
            affected_files=affected_files,
        )

    return None

if WATCHDOG_AVAILABLE:
    class SecretFileHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory or event.src_path.endswith((".tmp", ".cache", ".pyc")):
                return
            file_path = event.src_path
            findings = check_file_for_secrets(file_path)
            if findings:
                # Original terminal log output (unchanged)
                print(f"\nKEYSHIELD ALERT: Secret detected in modified file!")
                print(f"File Path: {file_path}")
                for item in findings:
                    print(f"Type: {item.provider} | Masked Secret: {item.masked_value}")

                # Show desktop popup for each secret found
                for finding in findings:
                    show_desktop_popup(finding)


if __name__ == "__main__":
    if not WATCHDOG_AVAILABLE:
        print("Error: watchdog package is required for file monitoring")
        print("Install it with: pip install watchdog")
        sys.exit(1)

    path = os.getcwd()
    event_handler = SecretFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"KeyShield dynamic monitor started", flush=True)
    print(f"Watching directory: {path}", flush=True)
    print("Save any file to trigger scan. Press Ctrl+C to exit.\n", flush=True)

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()

