import os

valid_molt_types = {
    "Primary", "Subject", "Instruction", "Philosophy",
    "Blueprint", "Directive", "Trigger", "Merge", "Off"
}

root = os.path.join("data", "blocks")
misfiled_blocks = []

for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith(".block.json"):
            full_path = os.path.join(dirpath, filename)
            relative_dir = os.path.relpath(dirpath, root)

            if relative_dir not in valid_molt_types:
                misfiled_blocks.append(full_path)

if misfiled_blocks:
    print("❌ Misfiled blocks found (not inside canonical folders):\n")
    for path in misfiled_blocks:
        print("  -", path)
else:
    print("✅ All blocks are stored in correct molt_type folders.")