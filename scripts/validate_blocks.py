#!/usr/bin/env python3
import json
import glob
import sys
from jsonschema import Draft7Validator

# Point this at your schema files
SCHEMA_PATH   = 'schema/cantocore_block_schema.json'
BLOCKS_GLOB   = 'blocks/**/*.json'

def load_schema(path):
    with open(path) as f:
        return json.load(f)

def load_blocks(pattern):
    files = glob.glob(pattern, recursive=True)
    blocks = []
    for fn in files:
        with open(fn) as f:
            try:
                data = json.load(f)
                blocks.append((fn, data))
            except Exception as e:
                print(f"[ERROR] Invalid JSON in {fn}: {e}")
                sys.exit(1)
    return blocks

def validate(schema, blocks):
    validator = Draft7Validator(schema)
    errors = False
    for fn, block in blocks:
        for err in validator.iter_errors(block):
            print(f"[SCHEMA ERROR] {fn} -> {err.message}")
            errors = True
    if errors:
        sys.exit(1)
    print(f"All {len(blocks)} block files conform to schema.")

def main():
    schema = load_schema(SCHEMA_PATH)
    blocks = load_blocks(BLOCKS_GLOB)
    validate(schema, blocks)

if __name__ == '__main__':
    main()
