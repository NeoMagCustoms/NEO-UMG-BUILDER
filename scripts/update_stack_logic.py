import os
import json

# Directory containing all .block.json files
BLOCKS_DIR = "data/blocks"

# Stack vertical order for UMG logic
STACK_PRIORITY = {
    "Primary": 0,
    "Subject": 1,
    "Instruction": 2,
    "Directive": 3,
    "Philosophy": 4,
    "Blueprint": 5,
    "Trigger": 10,
    "Deployment": 11,
    "Off": 99
}

# Who can snap to who (horizontal logic)
SNAP_ACCEPTS = {
    "Primary": ["Subject", "Instruction", "Directive", "Philosophy", "Blueprint"],
    "Subject": ["Instruction", "Directive", "Philosophy", "Blueprint"],
    "Instruction": ["Blueprint", "Directive", "Philosophy"],
    "Directive": ["Instruction", "Philosophy"],
    "Philosophy": ["Blueprint", "Instruction", "Directive"],
    "Blueprint": [],
    "Trigger": ["Primary"],
    "Deployment": ["Primary", "Instruction"],
    "Off": []
}

# Collect broken blocks if any
broken_blocks = []

def update_block_logic(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            block = json.load(f)

        molt_type = block.get("molt_type", None)
        if not molt_type:
            broken_blocks.append({"path": path, "error": "Missing molt_type"})
            return

        # Assign stack priority
        block["stack_priority"] = STACK_PRIORITY.get(molt_type, 99)

        # Snap config setup
        if "snap_config" not in block:
            block["snap_config"] = {}

        block["snap_config"]["accepts"] = SNAP_ACCEPTS.get(molt_type, [])
        block["snap_config"]["priority"] = block["stack_priority"]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(block, f, indent=2)

    except Exception as e:
        broken_blocks.append({"path": path, "error": str(e)})

# Walk through all block files
for root, _, files in os.walk(BLOCKS_DIR):
    for file in files:
        if file.endswith(".block.json"):
            full_path = os.path.join(root, file)
            update_block_logic(full_path)

# Final report
if broken_blocks:
    print("⚠️ Some blocks could not be updated:")
    for entry in broken_blocks:
        print(entry)
else:
    print("✅ All blocks updated with stack logic.")
