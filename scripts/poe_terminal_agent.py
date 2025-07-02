# scripts/poe_terminal_agent.py

from openai import OpenAI
import os
import sys
import subprocess

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load prompt from command line or use fallback
user_prompt = " ".join(sys.argv[1:]) or "List the UMG MOLT types and explain merge priority."

# Optional: inject system instructions from file
system_instructions = """
You are PoeUMG — a recursive modular agent inside a UMG-based Git environment.
Follow modular logic rules. You may respond with bash code blocks if necessary.
"""

# Build conversation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_prompt}
    ]
)

reply = response.choices[0].message.content
print(f"\n🧠 Poe Says:\n{reply}\n")

# Optional shell execution for ```bash blocks
if "```bash" in reply:
    command = reply.split("```bash")[1].split("```")[0].strip()
    print(f"\n🔧 Running: {command}\n")
    subprocess.run(command, shell=True)

