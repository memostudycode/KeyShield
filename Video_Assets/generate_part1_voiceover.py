import pyttsx3

# Script for Part 1 (Slides 1-8)
part1_script = """
Welcome to KeyShield—the proactive, local protection system against API key leakage for AI developers.
In this video, we’ll introduce the problem, our solution, and a live demo of how KeyShield works.

AI developers face a critical risk: API keys are often leaked accidentally in code commits or files.
Existing tools like TruffleHog or GitGuardian only detect secrets after they’re exposed—by then, it’s too late.

With the explosive growth of LLM usage, more developers are juggling multiple API keys.
Solo devs and small teams lack dedicated security infrastructure, making accidental exposure a growing threat.

KeyShield solves this with a two-layer defense: First, a real-time file monitor that triggers instant desktop alerts
when API keys are detected in saved files. Second, a git pre-commit hook that blocks commits containing secrets before they’re pushed online.

KeyShield is privacy-first: it never logs keystrokes, stores secrets, or sends data to the cloud.
It’s lightweight, fast, and runs entirely on your local machine.
"""

# Save voiceover for Part 1
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
engine.save_to_file(part1_script, 'C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\part1_voiceover.mp3')
engine.runAndWait()

print("Part 1 voiceover generated.")