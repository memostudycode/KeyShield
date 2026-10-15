"""Secret detection and masking for KeyShield.

Detects API keys from multiple LLM providers and replaces the secret body with
``****`` while keeping the prefix, so users can still see *what kind* of key
was redacted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MASK = "****"

# Minimum number of characters after the prefix before we treat a token as a
# key. Keeps ordinary words such as "sk-learn" or "task-list" from matching.
_MIN_BODY_LEN = 10

# Characters allowed inside a key body. Real keys use letters, digits, "_" and
# "-" (e.g. "sk-proj-...", "sk-ant-api03-...", "tvly-dev-...").
_BODY = rf"[A-Za-z0-9_\-]{{{_MIN_BODY_LEN},}}"

# Configurable provider patterns. Format: (prefix_pattern, provider_name, display_prefix)
# New providers can be added here without changing core logic.
# IMPORTANT: Longer prefixes must come before shorter ones (e.g., sk-ant- before sk-)
_PROVIDER_PATTERNS = [
    # Anthropic Claude (must come before sk-)
    (r"sk-ant-", "anthropic", "sk-ant-"),
    # OpenAI
    (r"sk-", "openai", "sk-"),
    # Tavily
    (r"tvly-", "tavily", "tvly-"),
    # Google AI / Gemini
    (r"AIza", "google", "AIza"),
    (r"GOOG", "google", "GOOG"),
    # Cohere
    (r"cohere-", "cohere", "cohere-"),
    # Hugging Face
    (r"hf_", "huggingface", "hf_"),
    # Mistral AI
    (r"md-", "mistral", "md-"),
    # Together AI
    (r"together_", "together", "together_"),
    # Perplexity
    (r"pplx-", "perplexity", "pplx-"),
    # Replicate
    (r"r8_", "replicate", "r8_"),
]

# Build combined regex pattern from all providers
_PREFIX_CHOICES = "|".join(prefix for prefix, _, _ in _PROVIDER_PATTERNS)
_KEY_PATTERN = re.compile(
    rf"(?<![A-Za-z0-9_\-])(?P<prefix>{_PREFIX_CHOICES})(?P<body>{_BODY})"
)

# Map prefixes to provider names for output
_KEY_TYPES = {prefix: provider for prefix, provider, _ in _PROVIDER_PATTERNS}
# Map prefixes to display prefixes for masking
_DISPLAY_PREFIXES = {prefix: display for prefix, _, display in _PROVIDER_PATTERNS}


@dataclass(frozen=True)
class Finding:
    """One detected key. Never contains the raw secret."""

    type: str  # "sk" or "tvly"
    start: int  # offset in the ORIGINAL text
    end: int  # exclusive offset in the ORIGINAL text
    masked: str  # e.g. "sk-****"


def scan(text: str) -> tuple[str, list[Finding]]:
    """Return ``(masked_text, findings)`` for ``text``.

    Offsets in each finding refer to the original input text.
    """
    if not text:
        return "", []

    findings: list[Finding] = []

    def _replace(match: re.Match[str]) -> str:
        prefix = match.group("prefix")
        # Use display prefix for masking (e.g., "sk-ant-" -> "sk-ant-****")
        display_prefix = _DISPLAY_PREFIXES.get(prefix, prefix)
        masked = f"{display_prefix}{MASK}"
        findings.append(
            Finding(type=_KEY_TYPES[prefix], start=match.start(), end=match.end(), masked=masked)
        )
        return masked

    masked_text = _KEY_PATTERN.sub(_replace, text)
    return masked_text, findings


def get_supported_providers() -> list[dict[str, str]]:
    """Return list of supported API key providers with their patterns.

    Returns a list of dicts with keys: provider, prefix, example.
    """
    return [
        {"provider": provider, "prefix": prefix, "example": f"{prefix}{'x' * _MIN_BODY_LEN}"}
        for prefix, provider, _ in _PROVIDER_PATTERNS
    ]
