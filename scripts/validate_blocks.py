#!/usr/bin/env python3
import json
import glob
import sys
from jsonschema import Draft7Validator

# Update these two paths:
SCHEMA_PATH = 'docs/umg_block_schema.json'     # your updated v2.0 schema file
BLOCKS_GLOB = 'data/blocks/**/*.block.json'    # match all .block.json files under data/blocks

def load_schema(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load schema at {path}: {e}")
        sys.exit(1)


def load_blocks(pattern):
    files = glob.glob(pattern, recursive=True)
    if not files:
        print(f"⚠️  No block files found with pattern: {pattern}")
    blocks = []
    for fn in files:
        try:
            with open(fn, 'r') as f:
                data = json.load(f)
            blocks.append((fn, data))
        except Exception as e:
            print(f"❌ Invalid JSON in {fn}: {e}")
            sys.exit(1)
    return blocks


def validate(schema, blocks):
    validator = Draft7Validator(schema)
    errors = False
    for fn, block in blocks:
        for err in validator.iter_errors(block):
            loc = " > ".join(str(x) for x in err.path) or '(root)'
            print(f"[SCHEMA ERROR] {fn} at {loc}: {err.message}")
            errors = True
    if errors:
        print("\n❌ Some blocks failed validation.")
        sys.exit(1)
    print(f"✅ All {len(blocks)} block files conform to schema.")


def main():
    schema = load_schema(SCHEMA_PATH)
    blocks = load_blocks(BLOCKS_GLOB)
    validate(schema, blocks)


if __name__ == '__main__':
    main()
