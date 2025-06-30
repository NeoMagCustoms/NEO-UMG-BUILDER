import json
import os
import re
import sys
from pathlib import Path

VALID_MOLT_TYPES = [
    "Primary", "Subject", "Instruction", "Blueprint", "Philosophy",
    "Directive", "Trigger", "Deployment", "Off"
]

def safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def unpack_blocks(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            blocks = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format in {json_path}: {e}")
        return

    base_dir = Path("data/blocks")
    count = 0

    for block in blocks:
        try:
            block_id = block["block_id"]
            molt_type = block["molt_type"]

            if molt_type not in VALID_MOLT_TYPES:
                print(f"⚠️ Skipped: Invalid molt_type '{molt_type}' in {block_id}")
                continue

            out_dir = base_dir / molt_type
            out_dir.mkdir(parents=True, exist_ok=True)

            file_name = f"{safe_filename(block_id)}.block.json"
            file_path = out_dir / file_name

            if file_path.exists():
                print(f"⚠️ Skipped: {file_name} already exists.")
                continue

            with open(file_path, 'w', encoding='utf-8') as f_out:
                json.dump(block, f_out, indent=2, ensure_ascii=False)
                count += 1

        except Exception as e:
            print(f"❌ Error processing block: {e}")

    print(f"\n✅ {count} blocks unpacked successfully into /data/blocks/<molt_type>/ folders.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a .json file to unpack.\nUsage: python scripts/unpack_blocks.py your_file.json")
    else:
        unpack_blocks(sys.argv[1])
