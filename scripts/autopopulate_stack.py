import os
import json

BLOCKS_DIR = "data/blocks"
TEMPLATE_TAG = "STACK.FILL.TEMPLATE"  # Base filter for matching stack blocks

# Optional: define what types you want per stack
DESIRED_ORDER = ["Primary", "Subject", "Instruction", "Directive", "Philosophy", "Blueprint"]

def load_blocks():
    """Load all valid .block.json files from data/blocks/."""
    blocks = []
    for root, _, files in os.walk(BLOCKS_DIR):
        for file in files:
            if file.endswith(".block.json"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        data["__path"] = path  # Add source path for reference
                        blocks.append(data)
                    except json.JSONDecodeError:
                        print(f"❌ Invalid JSON in {path}")
    return blocks

def match_template_blocks(all_blocks, template_id=None):
    """Filter and return blocks that match a given template via cantocore or tags."""
    matched = []
    for block in all_blocks:
        cantocore = block.get("cantocore", "")
        tags = block.get("tags", [])
        if template_id:
            if template_id in cantocore or template_id in tags:
                matched.append(block)
        else:
            if TEMPLATE_TAG in cantocore:
                matched.append(block)
    return matched

def sort_blocks_by_stack_order(blocks):
    """Sort matched blocks by stack priority."""
    priority = {
        "Primary": 0, "Subject": 1, "Instruction": 2,
        "Directive": 3, "Philosophy": 4, "Blueprint": 5
    }
    return sorted(blocks, key=lambda b: priority.get(b.get("molt_type", ""), 99))

def autopopulate_stack(template_id=None):
    all_blocks = load_blocks()
    matched = match_template_blocks(all_blocks, template_id)
    stack = sort_blocks_by_stack_order(matched)
    print("\n🧠 Auto-Stack Build:")
    for b in stack:
        print(f" - [{b.get('molt_type', '?')}] {b.get('label', 'Unnamed')}  ({os.path.basename(b['__path'])})")

    return stack

# === EXECUTE ===
if __name__ == "__main__":
    # You can customize this string to match your stack pattern (or leave blank)
    autopopulate_stack(template_id="STACK.FILL.TEMPLATE.STARTUP")
