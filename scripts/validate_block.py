import os
import json
from pathlib import Path

BLOCKS_DIR = Path("data/blocks")
REQUIRED_FIELDS = [
    "block_id", "label", "category", "description", "molt_type", "tags",
    "cantocore", "snap_config", "merge_logic", "ledger", "display",
    "code_modules", "runtime_behavior_flags", "agent_orchestration",
    "integration_layer", "future_extensions", "example_block_data"
]

def validate_block(block_path):
    try:
        with open(block_path, 'r', encoding='utf-8') as f:
            block = json.load(f)
        missing = [key for key in REQUIRED_FIELDS if key not in block]
        if missing:
            print(f"❌ {block_path.name} missing fields: {missing}")
            return False
        return True
    except Exception as e:
        print(f"❌ Failed to load {block_path.name}: {e}")
        return False

def run_validation():
    total = 0
    passed = 0
    for molt_dir in BLOCKS_DIR.iterdir():
        if molt_dir.is_dir():
            for block_file in molt_dir.glob("*.block.json"):
                total += 1
                if validate_block(block_file):
                    passed += 1
    print(f"\n✅ Validation complete: {passed}/{total} blocks valid.")

if __name__ == "__main__":
    run_validation()
