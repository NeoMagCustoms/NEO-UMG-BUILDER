# poe_terminal_agent.py
import openai
import os
import sys

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get the user's full natural language prompt
user_prompt = " ".join(sys.argv[1:])

# Default if none provided
if not user_prompt:
    user_prompt = "List the UMG MOLT types and explain merge priority."

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "You are NeoPoeUMG — a modular recursive agent running inside a GitHub Codespace. "
                "You have access to the local filesystem, UMG logic blocks, and scripts like poe_exec.py and poe_git_commit.py. "
                "Your job is to interpret user requests, write or modify files, commit them, or trigger terminal commands safely. "
                "Never hallucinate paths. Only write or act on what exists unless instructed to create. "
                "If unsure, reply with a clarification question."
            )
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
)

print("\n🧠 Poe says:\n")
print(response.choices[0].message.content)
