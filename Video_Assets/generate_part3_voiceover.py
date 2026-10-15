import pyttsx3

# Script for Part 3 (Slides 9-16)
part3_script = """
Unlike post-commit tools, KeyShield is proactive, local, and privacy-focused.
It’s the only solution that stops leaks before they happen—without cloud dependency or invasive monitoring.

Our roadmap includes Linux/Mac support, enterprise features, and CI/CD integrations.
We’re also expanding our pattern library to cover cloud providers like AWS and Azure.

KeyShield aims to reduce API key leakage by 80% for individual developers.
It eliminates remediation time and fosters a security-first culture in AI development.

To summarize: KeyShield is proactive, privacy-first, and developer-friendly.
It’s the lightweight, local solution AI developers need to prevent secrets from leaking—before it’s too late.

Thank you for watching! Try KeyShield today, join our community,
and help us make AI development safer for everyone. Built for the AI GENESIS Hackathon.
"""

# Save voiceover for Part 3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
engine.save_to_file(part3_script, 'C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\part3_voiceover.mp3')
engine.runAndWait()

print("Part 3 voiceover generated.")