# scripts/poe_git_commit.py
import os
import subprocess
import sys

def run_git_command(command, cwd="."):
    result = subprocess.run(command, shell=True, cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip(), result.stderr.strip()

def commit_changes(message="Update from NeoPoeUMG"):
    os.environ["GIT_AUTHOR_NAME"] = "NeoPoeUMG"
    os.environ["GIT_AUTHOR_EMAIL"] = "poe@neomag.ai"

    run_git_command("git add .")
    stdout, stderr = run_git_command(f"git commit -m \"{message}\"")
    
    if "nothing to commit" in stdout.lower():
        return "No changes to commit."
    elif stderr:
        return f"Error during commit:\n{stderr}"
    
    out, err = run_git_command("git push origin main")
    return out if not err else f"Push failed:\n{err}"

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Sync by Poe"
    print(commit_changes(msg))
