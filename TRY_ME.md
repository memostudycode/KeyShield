# KeyShield - Quick Test Guide

This guide helps you quickly test all KeyShield features in under 5 minutes.

## Prerequisites

- Python 3.8 or higher installed
- Git installed (for pre-commit hook test)

## Setup (2 minutes)

```bash
# Navigate to KeyShield directory
cd KeyShield
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## Test 1: Real-Time File Monitor (1 minute)

**Objective**: See desktop popup warning when saving a file with API key

### Steps:

1. **Start the monitor** in Terminal 1:
```bash
python -m app.monitor
```

You should see:
```
KeyShield dynamic monitor started
Watching directory: C:xxx\Desktop\KeyShield
Save any file to trigger scan. Press Ctrl+C to exit.
```

2. **Create a test file** in your editor:
```bash
# Create test_file.py
API_KEY = "sk-A1b2C3d4E5f6G7h8I9j0KlMn"
print("This file contains a fake API key")
```

3. **Save the file**

4. **Expected Result**:
   - Terminal shows alert with file path and masked secret
   - **Desktop popup window appears** with warning details

5. **Clean up**:
```bash
rm test_file.py
```

6. **Stop monitor**: Press `Ctrl+C` in Terminal 1

---

## Test 2: Git Pre-Commit Hook (1 minute)

**Objective**: See commit blocking when secrets are detected

### Steps:

1. **Install the pre-commit hook**:
```bash
cp pre_commit_hook.py .git/hooks/pre-commit
```

2. **Create a file with secret**:
```bash
# Create secret_config.py
OPENAI_KEY = "sk-A1b2C3d4E5f6G7h8I9j0KlMn"
GOOGLE_KEY = "AIzaA1b2C3d4E5f6G7h8I9j0KlMn"
```

3. **Stage the file**:
```bash
git add secret_config.py
```

4. **Try to commit**:
```bash
git commit -m "Add config with secrets"
```

5. **Expected Result**:
   - Commit is **blocked**
   - Terminal shows error with affected files
   - **Desktop popup appears** with warning

6. **Remove the secret** and retry:
```bash
# Edit secret_config.py to remove secrets
OPENAI_KEY = "sk-****"
GOOGLE_KEY = "AIza****"

git add secret_config.py
git commit -m "Add config (masked)"
```

7. **Expected Result**: Commit succeeds

8. **Clean up**:
```bash
rm secret_config.py
git reset --soft HEAD~1
```

---

## Test 3: Web UI - Manual Text Masking (1 minute)

**Objective**: Use the web interface to mask text

### Steps:

1. **Start the web server**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Open browser**: Navigate to `http://localhost:8000`

3. **Test masking**:
   - Paste text with API key in left box:
     ```
     My API key is sk-A1b2C3d4E5f6G7h8I9j0KlMn
     ```
   - Click "Mask" or see automatic masking
   - Right box shows: `My API key is sk-****`

4. **Test with multiple providers**:
   ```
   OpenAI: sk-A1b2C3d4E5f6G7h8I9j0KlMn
   Anthropic: sk-ant-A1b2C3d4E5f6G7h8I9j0KlMn
   Google: AIzaA1b2C3d4E5f6G7h8I9j0KlMn
   HuggingFace: hf_A1b2C3d4E5f6G7h8I9j0KlMn
   ```
   - All should be masked with `****`

5. **Stop server**: Press `Ctrl+C`

---

## Test 4: API Endpoints (Optional - 30 seconds)

### Test via curl:

```bash
# Test masking endpoint
curl -X POST http://localhost:8000/api/mask \
  -H "Content-Type: application/json" \
  -d '{"text": "key=sk-A1b2C3d4E5f6G7h8I9j0KlMn"}'

# Expected response:
# {"masked_text":"key=sk-****","count":1,"findings":[...]}

# Test providers endpoint
curl http://localhost:8000/api/providers

# Expected response: List of all supported providers
```

---

## Supported API Key Patterns

Try these in any test:

- **OpenAI**: `sk-xxxx`
- **Anthropic**: `sk-ant-xxxx`
- **Google**: `AIzaxxxx` or `GOOGxxxx`
- **Cohere**: `cohere-xxxx`
- **Hugging Face**: `hf_xxxx`
- **Mistral**: `md-xxxx`
- **Together**: `together_xxxx`
- **Perplexity**: `pplx-xxxx`
- **Replicate**: `r8_xxxx`
- **Tavily**: `tvly-xxxx`

Note: `xxxx` must be at least 10 characters from `[A-Za-z0-9_-]`

---

## Troubleshooting

**Popup not appearing?**
- Ensure tkinter is installed (built-in with Python)
- Check if firewall is blocking popup windows
- Try running: `python -c "import tkinter; print('OK')"`

**Monitor not detecting file changes?**
- Ensure you're editing files in the monitored directory
- Check that file extensions are not excluded (.tmp, .cache, .pyc)
- Wait 1-2 seconds after saving for detection

**Pre-commit hook not working?**
- Ensure `.git/hooks/pre-commit` is executable
- Check Python is in your system PATH
- Verify dependencies are installed in activated venv

---

## Clean Up After Testing

```bash
# Remove test files
rm -f test_file.py secret_config.py

# Remove pre-commit hook
rm -f .git/hooks/pre-commit

# Deactivate virtual environment
deactivate
```

---

## What You Should See

✅ **Real-time alert**: Desktop popup appears immediately when saving file with secret
✅ **Commit blocking**: Git commit fails with error when secrets are staged
✅ **Text masking**: Web UI masks all detected API keys with `****`
✅ **Zero persistence**: No secrets are stored or logged anywhere

## Next Steps

- Read [README.md](README.md) for project overview and market analysis
- Read [README_detailed.md](README_detailed.md) for technical documentation
- Check `tests/` directory for unit tests

---

**Total Testing Time**: ~5 minutes
**Difficulty**: Beginner-friendly
