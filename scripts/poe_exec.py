# scripts/poe_exec.py

import subprocess
import sys

def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print("⏱ Command:", command)
        print("✅ Output:\n", result.stdout)
        if result.stderr:
            print("⚠️ Error:\n", result.stderr)
    except Exception as e:
        print("❌ Exception:", str(e))

if __name__ == "__main__":
    user_command = " ".join(sys.argv[1:])
    run_shell_command(user_command)
