import json
import subprocess
import sys
import os
from pathlib import Path

TODO_PATH = 'docs/AI_TODO.json'
VALIDATOR = 'python3 scripts/validate_blocks.py'
COMMIT_SCRIPT = './scripts/poe_commit.sh'


def load_tasks(path=TODO_PATH):
    with open(path, 'r') as f:
        return json.load(f)


def run_validation():
    print('Running schema validation…')
    result = subprocess.run(VALIDATOR.split(), capture_output=True, text=True)
    if result.returncode != 0:
        print('Validation errors:\n', result.stdout, result.stderr)
        sys.exit(1)
    print('Validation passed.')


def add_block(task):
    block_id = task.get('block_id')
    category = task.get('category')
    filename = f"blocks/{category}/{block_id}.json"
    print(f"Creating placeholder block: {filename}")
    placeholder = {
        "block_id": block_id,
        "label": task.get('label', block_id),
        "category": category,
        "molt_type": task.get('molt_type', 'Instruction'),
        "description": task.get('description', ''),
        "body": []
    }
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(placeholder, f, indent=2)
    print(f"Block {block_id} created.")
    return filename


def commit_changes(files, message):
    args = [COMMIT_SCRIPT, files, message]
    subprocess.run(args, check=True)
    print(f"Committed changes: {message}")


def evaluate_repo():
    print("📂 Repo structure overview:")
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            path = os.path.join(root, name)
            if "node_modules" not in path and ".git" not in path:
                print("-", path)


def handle_write_file(task):
    path = task['path']
    code = task['code']
    message = task.get('message', f"Add file {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(code)
    print(f"✅ Wrote file: {path}")
    commit_changes(path, message)


def handle_move_file(task):
    src = task['from']
    dest = task['to']
    message = task.get('message', f"Move file {src} to {dest}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(src):
        os.rename(src, dest)
        print(f"✅ Moved {src} → {dest}")
        commit_changes(dest, message)
    else:
        print(f"⚠️  Source file does not exist: {src}")


def main():
    tasks = load_tasks()
    changed_files = []
    for t in tasks:
        action = t.get('task')
        if action == 'add block':
            f = add_block(t)
            changed_files.append(f)
        elif action == 'validate schema':
            run_validation()
        elif action == 'setup commit script':
            print('Ensuring commit script is executable…')
            subprocess.run(['chmod', '+x', 'scripts/poe_commit.sh'], check=True)
        elif action == 'evaluate repo':
            evaluate_repo()
        elif action == 'write file':
            handle_write_file(t)
        elif action == 'move file':
            handle_move_file(t)
        else:
            print(f"⚠️  Unknown task: {action}")

    if changed_files:
        ids = ','.join([os.path.basename(f) for f in changed_files])
        commit_message = f"[Poe] Added blocks: {ids}"
        commit_changes(' '.join(changed_files), commit_message)


if __name__ == '__main__':
    main()
