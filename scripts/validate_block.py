import os, json

REQUIRED_FIELDS = [
    "block_id", "label", "category", "molt_type", "tags",
    "ledger", "editable_fields", "cantocore", "display"
]

root = "data/blocks"
errors = []

for dirpath, _, filenames in os.walk(root):
    for f in filenames:
        if f.endswith(".block.json"):
            full_path = os.path.join(dirpath, f)
            try:
                with open(full_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                for field in REQUIRED_FIELDS:
                    if field not in data:
                        errors.append(f"❌ Missing `{field}` in: {full_path}")
            except Exception as e:
                errors.append(f"❌ Invalid JSON in: {full_path} — {e}")

print(f"\n✅ Validation complete: {len(errors)} issues found.\n")
for err in errors:
    print(err)
