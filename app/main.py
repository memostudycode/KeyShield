"""KeyShield FastAPI service: a tiny web UI and a JSON masking endpoint."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.detector import get_supported_providers, scan
from app.monitor import check_git_staged_files, scan_current_directory

# Large enough for pasted logs/configs, small enough to stop abuse of a demo box.
MAX_INPUT_CHARS = 100_000

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="KeyShield", version="0.1.0")


class MaskRequest(BaseModel):
    text: str = Field(..., max_length=MAX_INPUT_CHARS)


class FindingOut(BaseModel):
    type: str
    start: int
    end: int
    masked: str


class MaskResponse(BaseModel):
    masked_text: str
    count: int
    findings: list[FindingOut]


class ProviderInfo(BaseModel):
    provider: str
    prefix: str
    example: str


class SecretFindingOut(BaseModel):
    file_path: str
    provider: str
    masked_value: str
    line_number: int | None = None


class WarningContextOut(BaseModel):
    operation: str
    secrets_found: list[SecretFindingOut]
    affected_files: list[str]



@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html", media_type="text/html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/mask", response_model=MaskResponse)
def mask(req: MaskRequest) -> MaskResponse:
    # The input is never logged or stored: it may contain live secrets.
    masked_text, findings = scan(req.text)
    return MaskResponse(
        masked_text=masked_text,
        count=len(findings),
        findings=[FindingOut(**f.__dict__) for f in findings],
    )


@app.get("/api/providers", response_model=list[ProviderInfo])
def list_providers() -> list[ProviderInfo]:
    """List all supported API key providers and their patterns."""
    providers = get_supported_providers()
    return [ProviderInfo(**p) for p in providers]


@app.get("/api/monitor/git", response_model=WarningContextOut | dict)
def check_git() -> dict:
    """Check git staged files for secrets before push."""
    context = check_git_staged_files()
    if context:
        return WarningContextOut(
            operation=context.operation,
            secrets_found=[SecretFindingOut(**s.__dict__) for s in context.secrets_found],
            affected_files=list(context.affected_files),
        )
    return {"status": "safe", "message": "No secrets found in staged files"}


@app.get("/api/monitor/scan", response_model=WarningContextOut | dict)
def scan_directory() -> dict:
    """Scan current directory for secrets."""
    context = scan_current_directory()
    if context:
        return WarningContextOut(
            operation=context.operation,
            secrets_found=[SecretFindingOut(**s.__dict__) for s in context.secrets_found],
            affected_files=list(context.affected_files),
        )
    return {"status": "safe", "message": "No secrets found in directory"}
