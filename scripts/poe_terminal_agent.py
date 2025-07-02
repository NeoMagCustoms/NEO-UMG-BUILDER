import openai
import os
import sys
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")

user_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "List the UMG MOLT types and explain merge priority."

system_instructions = """
You are PoeUMG, an autonomous terminal agent.
You are permitted to:
- Read, write, move, and list files inside the repo
- Understand the UMG block system and the file tree
- Generate and run valid bash and python commands
- Respond using markdown when helpful
- Only execute safe commands and refuse destructive ones

Context:
- Workspace = ~/workspaces/NEO-UMG-BUILDER
- Blocks are in: data/blocks/
- Core logic is in: poe_core/
"""

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_prompt}
    ]
)

reply = response.choices[0].message.content
print(f"\n🧠 Poe Says:\n{reply}\n")

# 🔧 Optionally detect & execute shell code blocks
if "```bash" in reply:
    command = reply.split("```bash")[1].split("```")[0].strip()
    print(f"🛠️  Running: {command}\n")
    subprocess.run(command, shell=True)
