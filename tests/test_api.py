from fastapi.testclient import TestClient

from app.main import MAX_INPUT_CHARS, app

client = TestClient(app)

BODY = "Zz9Yy8Xx7Ww6Vv5Uu4Tt3Ss2"  # clearly fake filler


def test_index_serves_ui():
    res = client.get("/")
    assert res.status_code == 200
    assert 'id="input"' in res.text and 'id="output"' in res.text


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_mask_endpoint():
    text = "openai=" + "sk-" + BODY + " tavily=" + "tvly-" + BODY
    res = client.post("/api/mask", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["masked_text"] == "openai=sk-**** tavily=tvly-****"
    assert data["count"] == 2
    assert BODY not in res.text  # raw secret never echoed back


def test_mask_endpoint_no_keys():
    res = client.post("/api/mask", json={"text": "hello world"})
    assert res.json() == {"masked_text": "hello world", "count": 0, "findings": []}


def test_rejects_missing_text():
    assert client.post("/api/mask", json={}).status_code == 422


def test_rejects_oversized_input():
    res = client.post("/api/mask", json={"text": "a" * (MAX_INPUT_CHARS + 1)})
    assert res.status_code == 422


def test_list_providers():
    res = client.get("/api/providers")
    assert res.status_code == 200
    providers = res.json()
    assert isinstance(providers, list)
    assert len(providers) > 2  # More than just sk- and tvly-
    provider_names = {p["provider"] for p in providers}
    assert "openai" in provider_names
    assert "anthropic" in provider_names
    assert "google" in provider_names


def test_check_git_endpoint():
    res = client.get("/api/monitor/git")
    assert res.status_code == 200
    data = res.json()
    # Should return either safe status or warning context
    assert "status" in data or "operation" in data


def test_scan_directory_endpoint():
    res = client.get("/api/monitor/scan")
    assert res.status_code == 200
    data = res.json()
    # Should return either safe status or warning context
    assert "status" in data or "operation" in data
