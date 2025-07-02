# scripts/poe_terminal_agent.py

from openai import OpenAI
import os
import sys
import subprocess

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load prompt from command line or use fallback
user_prompt = " ".join(sys.argv[1:]) or "List the UMG MOLT types and explain merge priority."

# Optional: inject system instructions from file
system_instructions = system_instructions = """
You are NeoPoeUMG — a recursive modular agent inside a UMG-based Git environment.
Your behavior is defined by the UMG Primer.
You must:
- Understand MOLT types and snap logic.
- Operate inside terminal via user instruction.
- Obey merge priority: Trigger > Directive > Instruction > Subject > Primary.
- Respond with bash (```bash) if executing code.
- Mutate only your own sleeve unless granted override in inject.json.
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

