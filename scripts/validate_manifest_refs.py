import os
import json

BLOCKS_DIR = "data/blocks"
MANIFESTS_DIR = "apps/umg-builder-web/manifests"

def block_exists(block_id, molt_type):
    path = os.path.join(BLOCKS_DIR, molt_type, f"{block_id}.block.json")
    return os.path.isfile(path)

def validate_manifests():
    missing = []
    for root, _, files in os.walk(MANIFESTS_DIR):
        for file in files:
            if file.endswith(".json"):
                manifest_path = os.path.join(root, file)
                with open(manifest_path, "r", encoding="utf-8") as f:
                    try:
                        manifest = json.load(f)
                        for molt_type, ids in manifest.items():
                            for block_id in ids:
                                if not block_exists(block_id, molt_type):
                                    missing.append({
                                        "manifest": file,
                                        "molt_type": molt_type,
                                        "block_id": block_id
                                    })
                    except Exception as e:
                        missing.append({
                            "manifest": file,
                            "molt_type": "error",
                            "block_id": f"JSON ERROR: {e}"
                        })
    return missing

if __name__ == "__main__":
    result = validate_manifests()
    if not result:
        print("✅ All manifest block references are valid.")
    else:
        print("❌ Missing or invalid block references:")
        for entry in result:
            print(f"- Manifest: {entry['manifest']} | MOLT: {entry['molt_type']} | Block ID: {entry['block_id']}")
