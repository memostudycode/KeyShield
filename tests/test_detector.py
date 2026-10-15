"""Unit tests for the detector.

Fake keys are assembled at runtime (prefix + filler) so this file contains no
key-shaped literals that a secret scanner would flag.
"""

from app.detector import MASK, get_supported_providers, scan

SK = "sk-"
SK_ANT = "sk-ant-"
TVLY = "tvly-"
GOOGLE = "AIza"
GOOGLE_ALT = "GOOG"
COHERE = "cohere-"
HF = "hf_"
MISTRAL = "md-"
TOGETHER = "together_"
PERPLEXITY = "pplx-"
REPLICATE = "r8_"
BODY = "A1b2C3d4E5f6G7h8I9j0KlMn"  # 24 chars, clearly fake


def test_masks_sk_key():
    masked, findings = scan(f"key={SK}{BODY}")
    assert masked == f"key={SK}{MASK}"
    assert [f.type for f in findings] == ["openai"]


def test_masks_tvly_key():
    masked, findings = scan(f"{TVLY}{BODY}")
    assert masked == f"{TVLY}{MASK}"
    assert findings[0].type == "tavily"


def test_masks_project_and_dashed_variants_fully():
    text = f"{SK}proj-{BODY}_x-y {TVLY}dev-{BODY}"
    masked, findings = scan(text)
    assert masked == f"{SK}{MASK} {TVLY}{MASK}"
    assert len(findings) == 2
    assert [f.type for f in findings] == ["openai", "tavily"]


def test_multiple_keys_and_offsets_point_at_original_text():
    key1, key2 = f"{SK}{BODY}", f"{TVLY}{BODY}"
    text = f"a {key1} b\n{key2}"
    masked, findings = scan(text)
    assert masked == f"a {SK}{MASK} b\n{TVLY}{MASK}"
    assert text[findings[0].start:findings[0].end] == key1
    assert text[findings[1].start:findings[1].end] == key2


def test_raw_secret_not_present_in_findings():
    _, findings = scan(f"{SK}{BODY}")
    assert BODY not in repr(findings)


def test_ignores_short_tokens_and_words():
    text = "sk-learn is fine, so is tvly-x and sk-"
    masked, findings = scan(text)
    assert masked == text
    assert findings == []


def test_ignores_prefix_inside_other_words():
    text = f"risk-{BODY} and task-{BODY}"
    masked, findings = scan(text)
    assert masked == text
    assert findings == []


def test_key_in_quotes_and_json():
    text = f'{{"api_key": "{SK}{BODY}"}}'
    masked, _ = scan(text)
    assert masked == f'{{"api_key": "{SK}{MASK}"}}'


def test_empty_input():
    assert scan("") == ("", [])


def test_masks_anthropic_key():
    masked, findings = scan(f"{SK_ANT}{BODY}")
    assert masked == f"{SK_ANT}{MASK}"
    assert findings[0].type == "anthropic"


def test_masks_google_key():
    masked, findings = scan(f"{GOOGLE}{BODY}")
    assert masked == f"{GOOGLE}{MASK}"
    assert findings[0].type == "google"


def test_masks_google_alt_key():
    masked, findings = scan(f"{GOOGLE_ALT}{BODY}")
    assert masked == f"{GOOGLE_ALT}{MASK}"
    assert findings[0].type == "google"


def test_masks_cohere_key():
    masked, findings = scan(f"{COHERE}{BODY}")
    assert masked == f"{COHERE}{MASK}"
    assert findings[0].type == "cohere"


def test_masks_huggingface_key():
    masked, findings = scan(f"{HF}{BODY}")
    assert masked == f"{HF}{MASK}"
    assert findings[0].type == "huggingface"


def test_masks_mistral_key():
    masked, findings = scan(f"{MISTRAL}{BODY}")
    assert masked == f"{MISTRAL}{MASK}"
    assert findings[0].type == "mistral"


def test_masks_together_key():
    masked, findings = scan(f"{TOGETHER}{BODY}")
    assert masked == f"{TOGETHER}{MASK}"
    assert findings[0].type == "together"


def test_masks_perplexity_key():
    masked, findings = scan(f"{PERPLEXITY}{BODY}")
    assert masked == f"{PERPLEXITY}{MASK}"
    assert findings[0].type == "perplexity"


def test_masks_replicate_key():
    masked, findings = scan(f"{REPLICATE}{BODY}")
    assert masked == f"{REPLICATE}{MASK}"
    assert findings[0].type == "replicate"


def test_multiple_providers_in_one_text():
    text = f"{SK}{BODY} {SK_ANT}{BODY} {GOOGLE}{BODY} {HF}{BODY}"
    masked, findings = scan(text)
    assert len(findings) == 4
    assert [f.type for f in findings] == ["openai", "anthropic", "google", "huggingface"]


def test_get_supported_providers():
    providers = get_supported_providers()
    assert len(providers) > 2  # More than just sk- and tvly-
    provider_names = {p["provider"] for p in providers}
    assert "openai" in provider_names
    assert "anthropic" in provider_names
    assert "google" in provider_names
    assert "cohere" in provider_names
