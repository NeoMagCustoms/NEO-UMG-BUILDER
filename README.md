# 🧠 UMG Builder – Universal Modular Generation System

UMG Builder is a modular logic engine designed to power composable AI logic, chatbot scaffolds, semantic planning, and stack-based architecture.

This project enables:
- 💠 Modular `.block.json` logic units
- 📐 Snap / Stack / Merge logic via `snapMatrix.json` and `mergeMatrix.json`
- 🧱 Full UMG structure across Primary, Subject, Instruction, etc.
- ⚡️ Bolt-ready front-end builder with live block population
- 🔁 Philosophy + Directive overlays for tone and behavior

> "Build once. Snap forever."

---

## 🔗 Key Features

- **Static file logic** — no DB required
- **Fully recursive** block metadata system
- **Drag and drop support** (frontend-ready)
- **Script-powered logic injection** via Python

---

## 📁 Repo Structure

```plaintext
/data/blocks/               ← All UMG .block.json files (by molt_type)
/scripts/                   ← Python logic helpers
mergeMatrix.json            ← Merge priority + override rules
snapMatrix.json             ← Snap compatibility map
README.md                   ← This file
