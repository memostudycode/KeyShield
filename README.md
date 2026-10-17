![KeyShield Cover](KeyShield_cover.jpg)

# KeyShield

**Proactive Local Protection Against API Key Leakage for AI Developers**

## Short Description

Lightweight local security tool that prevents API key leakage by monitoring file changes in real-time and blocking git commits containing exposed secrets.

## Long Description

Individual AI developers working with large language models face critical security risks with API key management. Existing solutions either scan repositories after secrets are already exposed online (too late) or require invasive keyboard logging (privacy risk). KeyShield addresses this gap by providing proactive, local protection that detects secrets before they leave the developer's machine.

Target audience: Solo AI developers, small development teams, and researchers who work with multiple LLM providers and need a simple, non-intrusive way to prevent accidental secret leakage.

KeyShield's unique value proposition lies in its two-layer defense system: real-time desktop alerts when files are saved, and automatic git commit blocking. Unlike server-side middleware or post-commit scanners, KeyShield runs entirely on the local machine with zero persistence - secrets are never stored, logged, or cached. The tool currently supports 10 major LLM providers (OpenAI, Anthropic, Google, Cohere, Hugging Face, Mistral, Together AI, Perplexity, Replicate, Tavily) and can be easily extended with additional patterns.

## Technology & Category Tags

**Tags:** Security, Developer Tools, AI/ML, DevSecOps, Open Source

**Tech Stack:** Python, FastAPI, watchdog, tkinter, regex

## Problem

Individual AI developers face significant security risks with API key management:

- **Post-hoc scanning tools** only detect secrets after they've been committed and pushed online - by then, credentials may already be harvested
- **Credential theft tools** in the wild can rapidly scrape, validate, and misuse exposed keys from public repositories
- **No lightweight local solutions** exist that continuously monitor file changes without invasive keyboard logginG

## Solution

KeyShield provides **proactive, local prevention** rather than retrospective detection:

- **Layer 1: Real-Time File Monitor** - Runs quietly in the background, dynamically watching file modifications. When LLM API keys are detected, it immediately triggers a native desktop warning popup.
- **Layer 2: Git Pre-Commit Hook** - Final barrier that blocks git commits containing exposed secrets, preventing accidental uploads to GitHub.

**Key principle**: KeyShield only scans file content and never records or monitors keyboard input.

## Key Features

- **Multi-LLM API Key Recognition** - Detects keys from OpenAI, Anthropic, Google, Cohere, Hugging Face, Mistral, Together AI, Perplexity, and Replicate
- **Real-Time Desktop Alerts** - Native Windows popup warnings with file path, provider type, and masked secret
- **Git Pre-Commit Blocking** - Automatically blocks commits containing exposed secrets
- **Zero Persistence** - No database, no login, never stores or logs your secrets
- **Lightweight & Fast** - Minimal dependencies, instant detection on file save

## Quick Start

**For a complete hands-on testing guide, see [TRY_ME.md](TRY_ME.md)**

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd KeyShield

# Create a virtual environment (recommended)
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Real-Time Monitor

```bash
python -m app.monitor
```

The monitor will watch all files in the current directory and subdirectories. When you save a file containing an API key, you'll see an immediate desktop popup warning.

### Install Git Pre-Commit Hook

```bash
cp pre_commit_hook.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit  # Linux/Mac only
```

Now every `git commit` will be automatically scanned for secrets before proceeding.

### Demo Application

**Platform:** Local deployment (FastAPI + uvicorn)

**Access:** Run `uvicorn app.main:app --host 0.0.0.0 --port 8000` and open `http://localhost:8000`

The web UI allows manual text masking and provides API endpoints for integration.

### Running Results

**Desktop Alert Popup:**

![Alert Screenshot](.assets/alert_screenshot.png)

![Alert Screenshot 2](.assets/alert_screenshot_2.png)

**Web UI with Sample Keys:**

![KeyShield Web UI](.assets/keyshield_web_ui.png)

## Market Analysis

### Total Addressable Market (TAM)
- Global developer security tools market: $2.5B (2024)
- Growing at 15% CAGR due to increasing API usage and security awareness
- AI/ML development specifically drives significant demand

### Serviceable Addressable Market (SAM)
- Individual AI developers and small teams: ~500K developers globally
- Developers working with 3+ LLM providers: ~200K
- Open-source-first users who prefer local tools: ~100K

### Target Market
- Solo AI developers building LLM-powered applications
- Small development teams (1-10 developers) without dedicated security teams
- Researchers and academics working with multiple AI providers
- Open-source contributors who need to protect public repositories

### Revenue Streams

**Freemium Model**
- **Free Tier**: Basic local monitoring with 5 provider patterns, community support
- **Pro Tier ($9/month)**: All 10+ providers, priority support, custom pattern configuration, auto-masking features
- **Enterprise Tier ($49/month)**: Team dashboard, centralized policy management, SSO, audit logs, Slack/Teams integration

**Additional Revenue Sources**
- Custom pattern consulting for enterprise clients
- White-label licensing for security vendors
- Training and onboarding services

## Competitor Analysis


**TruffleHog**
- Strengths: Comprehensive scanning, large community
- Weaknesses: Post-commit only, requires manual triggering, server-based
- USP: Open source, extensive pattern database

**GitGuardian**
- Strengths: Enterprise features, CI/CD integration
- Weaknesses: Expensive, requires cloud service, complex setup
- USP: Enterprise-grade security dashboard

**Gitleaks**
- Strengths: Fast, customizable rules
- Weaknesses: CLI-only, no real-time alerts, post-commit focus
- USP: Lightweight, highly configurable

### KeyShield's Unique Selling Proposition

1. **Proactive vs Reactive**: Detects secrets before they leave local environment
2. **Zero Infrastructure**: Runs entirely on local machine, no cloud services
3. **Immediate Feedback**: Desktop popups provide instant awareness
4. **Privacy-First**: No keyboard logging, zero persistence
5. **Developer-Friendly**: Simple setup, minimal dependencies

## Future Prospects

### Scalability
- **Platform Expansion**: Linux/Mac desktop notifications, mobile companion app
- **Provider Expansion**: Add support for cloud providers (AWS, Azure, GCP)
- **Enterprise Features**: Team collaboration, policy enforcement, audit trails
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins plugins

### Impact Potential
- **Security Impact**: Reduce API key leakage incidents by 80% for individual developers
- **Developer Productivity**: Eliminate remediation time spent on leaked credentials
- **Open Source Community**: Foster a security-first culture in AI development
- **Educational Value**: Raise awareness about secret management best practices

### Growth Strategy
- **Phase 1**: Open source MVP with core features (current)
- **Phase 2**: Community building, contributor onboarding, pattern library expansion
- **Phase 3**: Pro tier launch with premium features
- **Phase 4**: Enterprise features and partnerships with LLM providers

## Security & Privacy

- **Zero Persistence**: Secrets are never stored, logged, or cached
- **Client-Side Only**: All detection happens in memory on your machine
- **No Keyboard Logging**: Only scans file content, never monitors input
- **Masked Output**: API responses only return masked values

## Limitations

- Hackathon MVP prototype
- Currently optimized for Windows (tkinter popups)
- Only detects known API key patterns
- Manual intervention required to actually mask files in place

## Documentation

For detailed technical documentation, API reference, testing instructions, and project structure, see [README_detailed.md](README_detailed.md)


For a quick hands-on testing guide, see [TRY_ME.md](TRY_ME.md)


For demo video,click https://github.com/user-attachments/assets/6d62f9b5-f2c9-46c2-a19a-0a32c5798729


For slide presentation,click
https://github.com/memostudycode/KeyShield/blob/main/KeyShield_Slide_Deck.pdf

## License

MIT License

## Team

I finished it with my agents team.

![Work Distribution](.assets/work_distribution.png)

## Acknowledgments

Built for ACT III Hackathon in 2026.
