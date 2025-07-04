#!/usr/bin/env python3
import os
import json
import glob
import datetime

# Constants
BLOCKS_DIR = "data/blocks"
TODAY = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# Fields to drop completely
UNWANTED_KEYS = [
    "ledger",
    "canto_overlay",
    "stack_priority",
    "merge_logic",
    "merge_origin",
    "example_block_data",
    "runtime_behavior_flags",
    "integration_layer",
    "agent_orchestration",
    "future_extensions"
]

# Default top-level values
TOP_LEVEL_DEFAULTS = {
    "domain":       "",
    "category":     "",
    "subcategory":  "General",
    "tags":         [],
    "editable_fields": [],
    "code_modules": [],
    "cantocore":    "UNSPECIFIED",
}

# Default display and style by MOLT
COLOR_BY_MOLT = {
    "Primary":    "blue",
    "Subject":    "green",
    "Instruction":"yellow",
    "Directive":  "purple",
    "Philosophy": "orange",
    "Blueprint":  "teal",
    "Merge":      "gray",
    "Trigger":    "red",
    "Off":        "gray"
}

# Which types each MOLT can snap to
SNAP_ACCEPTS = {
    "Primary":    ["Subject","Instruction","Directive","Philosophy","Blueprint"],
    "Subject":    ["Instruction","Directive","Philosophy","Blueprint"],
    "Instruction":["Blueprint","Directive","Philosophy"],
    "Directive":  ["Instruction","Philosophy"],
    "Philosophy": ["Blueprint","Instruction","Directive"],
    "Blueprint":  [],
    "Merge":      ["Instruction","Directive","Philosophy","Blueprint"],
    "Trigger":    ["Primary"],
    "Off":        []
}

# Default snap_config and merge_behavior
SNAP_DEFAULT = {
    "snap_to":  [],
    "accepts":  [],
    "order":    0,
    "priority": 0,
    "scope":    "local",
    "locked":   False
}
MERGE_DEFAULT = {
    "merge_as":            "instruction",
    "merge_strategy":      "append",
    "priority":            0,
    "conflict_resolution": "last_write_wins",
    "overrides":           []
}

def normalize_molt_type(mt: str) -> str:
    """Map legacy or invalid molt_type to our enum."""
    if mt == "Deployment":
        return "Instruction"
    if mt not in COLOR_BY_MOLT:
        return "Off"
    return mt

def autofill_block(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            blk = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON ({path}): {e}")
            return False

    changed = False

    # 1) Drop unwanted top-level keys
    for key in UNWANTED_KEYS:
        if key in blk:
            blk.pop(key)
            changed = True

    # 2) Normalize molt_type
    mt = normalize_molt_type(blk.get("molt_type", "Off"))
    if blk.get("molt_type") != mt:
        blk["molt_type"] = mt
        changed = True

    # 3) Fill top-level defaults
    for field, default in TOP_LEVEL_DEFAULTS.items():
        if field not in blk:
            # For domain/category, we leave domain/category=empty so we catch later
            blk[field] = default
            changed = True

    # 4) Ensure display.meta
    disp = blk.get("display", {})
    if "color" not in disp or not disp["color"]:
        disp["color"] = COLOR_BY_MOLT.get(mt, "gray")
        changed = True
    if "icon" not in disp or not disp["icon"]:
        disp["icon"] = "❓"
        changed = True
    if changed:
        blk["display"] = disp

    # 5) Ensure code_modules array
    if not isinstance(blk.get("code_modules"), list):
        blk["code_modules"] = []
        changed = True

    # 6) Snap and merge defaults
    sc = blk.get("snap_config", {}) or {}
    md = blk.get("merge_behavior", {}) or {}

    # Fill snap_config
    new_sc = SNAP_DEFAULT.copy()
    new_sc.update(sc)
    # set accepts based on molt_type if none defined
    if not new_sc["accepts"]:
        new_sc["accepts"] = SNAP_ACCEPTS.get(mt, [])
    blk["snap_config"] = new_sc
    changed = True

    # Fill merge_behavior
    new_mb = MERGE_DEFAULT.copy()
    new_mb.update(md)
    blk["merge_behavior"] = new_mb
    changed = True

    # 7) Stamp ledger.created_at if needed
    if "ledger" in blk:
        if blk["ledger"].get("created_at") in (None, "", "AUTO"):
            blk["ledger"]["created_at"] = TODAY
            changed = True

    # If we changed anything, write back
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(blk, f, indent=2, ensure_ascii=False)
        print(f"✅ Patched: {path}")

    return True

def walk_and_fix():
    total = 0
    updated = 0
    for fn in glob.glob(f"{BLOCKS_DIR}/**/*.block.json", recursive=True):
        if os.path.isfile(fn):
            total += 1
            if autofill_block(fn):
                updated += 1
    print(f"\n🔧 Done: {updated}/{total} blocks processed.")

if __name__ == "__main__":
    walk_and_fix()
