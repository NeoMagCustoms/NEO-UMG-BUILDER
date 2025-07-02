#!/usr/bin/env python3
import json, subprocess, sys, os

TODO_PATH     = 'docs/AI_TODO.json'
VALIDATOR_CMD = ['python3', 'scripts/validate_blocks.py']
COMMIT_SCRIPT = './scripts/poe_commit.sh'

def load_tasks(path=TODO_PATH):
    with open(path, 'r') as f:
        return json.load(f)

def run_validation():
    print('Running schema validation…')
    result = subprocess.run(VALIDATOR_CMD, capture_output=True, text=True)
    if result.returncode != 0:
        print('Validation errors:\n', result.stdout, result.stderr)
        sys.exit(1)
    print('Validation passed.')

def add_block(task):
    block_id  = task['block_id']
    category  = task['category']
    filename  = f"blocks/{category}/{block_id}.json"
    print(f"Creating placeholder block: {filename}")
    placeholder = {
      "block_id":     block_id,
      "label":        task.get('label', block_id),
      "category":     category,
      "molt_type":    task.get('molt_type', 'Instruction'),
      "description":  task.get('description', ''),
      "body":         []
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

def main():
    tasks = load_tasks()
    changed_files = []
    for t in tasks:
        action = t.get('task')
        if action == 'add block':
            f = add_block(t); changed_files.append(f)
        elif action == 'validate schema':
            run_validation()
        elif action == 'setup commit script':
            print('Ensuring commit script is executable…')
            subprocess.run(['chmod', '+x', 'scripts/poe_commit.sh'], check=True)
        else:
            print(f"Unknown task: {action}")

    if changed_files:
        ids = ','.join([os.path.basename(f) for f in changed_files])
        commit_message = f"[Poe] Added blocks: {ids}"
        commit_changes(' '.join(changed_files), commit_message)

if __name__ == '__main__':
    main()
