import os, json, datetime

BLOCKS_DIR = "data/blocks"
TODAY = datetime.datetime.utcnow().isoformat()

# Canonical fallback values
DEFAULTS = {
    "cantocore": "AUTO.FILL.CANTOCODE",
    "display": {"color": "gray", "icon": "zap"},
    "editable_fields": [],
    "tags": [],
    "ledger": {
        "originator": "Christopher L Haynes",
        "verified_by": "PoeUMG",
        "created_at": TODAY,
        "edit_log": []
    },
    "canto_overlay": {
        "snap_to": [],
        "preferred_context": "",
        "fit_score": 0.75,
        "display_hint": ""
    },
    "snap_config": {
        "accepts": [],
        "priority": 0
    },
    "merge_behavior": {
        "merge_as": "default",
        "merge_strategy": "layered_if_non_conflict",
        "merge_origin": "AUTO"
    }
}

COLOR_BY_MOLT = {
    "Primary": "blue",
    "Subject": "green",
    "Instruction": "yellow",
    "Philosophy": "orange",
    "Blueprint": "teal",
    "Directive": "purple",
    "Deployment": "gold",
    "Trigger": "red",
    "Off": "gray"
}

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

def autofill_block(path):
    with open(path, "r", encoding="utf-8") as f:
        try:
            block = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON: {path}")
            return False

    changed = False
    molt_type = block.get("molt_type", "Unknown")

    for field, default in DEFAULTS.items():
        if field not in block:
            block[field] = default
            changed = True

    # Display color
    if "display" in block and not block["display"].get("color"):
        block["display"]["color"] = COLOR_BY_MOLT.get(molt_type, "gray")
        changed = True

    # Snap config
    if "snap_config" in block and not block["snap_config"].get("accepts"):
        block["snap_config"]["accepts"] = SNAP_ACCEPTS.get(molt_type, [])
        changed = True

    # Timestamp replacement
    if block.get("ledger", {}).get("created_at") == "AUTO":
        block["ledger"]["created_at"] = TODAY
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(block, f, indent=2)
        print(f"✅ Updated: {path}")
    return True

def walk_and_fix():
    total, updated = 0, 0
    for root, _, files in os.walk(BLOCKS_DIR):
        for file in files:
            if file.endswith(".block.json"):
                total += 1
                path = os.path.join(root, file)
                if autofill_block(path):
                    updated += 1
    print(f"\n🔧 Done: {updated}/{total} blocks updated.")

if __name__ == "__main__":
    walk_and_fix()
