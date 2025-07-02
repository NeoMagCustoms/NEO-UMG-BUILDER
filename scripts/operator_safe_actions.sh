#!/bin/bash

# ┌────────────────────────────┐
# │ OPERATOR SAFE ACTION MENU │
# └────────────────────────────┘

# ✅ Basic Diagnostics

echo "\n🧪 OPERATOR DIAGNOSTIC START\n"

# 1. List top-level JSON files in root
echo "\n🗂 Root-level JSON files:"
ls -1 *.json || echo "(none found)"

# 2. List all block files
if [ -d "data/blocks" ]; then
  echo "\n🧱 Block JSONs in /data/blocks/:"
  ls -1 data/blocks/*.json || echo "(no blocks found)"
else
  echo "\n⚠️  data/blocks/ not found."
fi

# 3. Check for script files
if [ -d "scripts" ]; then
  echo "\n⚙️ Scripts in /scripts/:"
  ls -1 scripts/*.py || echo "(no scripts found)"
else
  echo "\n⚠️  scripts/ not found."
fi

# 4. Check Python version
echo "\n🐍 Python version:"
python --version 2>/dev/null || echo "Python not found"

# 5. Show active branch (for confirmation)
echo "\n🔁 Current Git branch:"
git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(not in a Git repo?)"

# ✅ Done

echo "\n✅ OPERATOR DIAGNOSTIC COMPLETE\n"
