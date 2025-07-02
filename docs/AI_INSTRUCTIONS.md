# Poe’s UMG & MOLT Quick Reference

## 1. UMG Core Concepts

* **Blocks**: Atomic units (JSON files) with:

  * `block_id`, `label`, `category`, `molt_type`, `body`
  * Optional: `code_modules`, `tags`, `editable_fields`, `stack`, `snap_config`, `merge_behavior`, `display`, `cantocore`
* **Schemas**:

  * Cantocore blocks validate against `schemas/cantocore_block_schema.json`
  * NeoCore blocks validate against `schemas/neocore_block_schema.json`

## 2. MOLT Roles (`molt_type`)

| Role        | Purpose                                |
| ----------- | -------------------------------------- |
| Primary     | Core directive                         |
| Subject     | Domain/context                         |
| Instruction | Action steps                           |
| Directive   | Overrides or system-level instructions |
| Blueprint   | Styling/structure templates            |
| Philosophy  | Tone/voice modifiers                   |
| Merge       | Combined auxiliary context             |
| Trigger     | Conditional execution                  |
| CodeBlock   | Raw code snippets (reserved)           |
| Off         | Disabled block                         |

## 3. Cantocore Syntax

* A single-line symbolic form:

  ```
  INSTRUCTION:SORT[ASC]={RUN.SORT.LIST}
  ```
* Use for quick human/AI readability. Always include in NeoCore blocks under `cantocore`.

## 4. Block Authoring Steps

1. **Create** `<blocks>/<category>/<block_id>.json`
2. **Fill** required fields and `body` entries.
3. **Embed** any documentation in `code_modules` (Markdown).
4. **Run** `scripts/validate_blocks.py` to ensure schema compliance.
5. **Stage & Commit** with `scripts/poe_commit.sh "Your message"`.

## 5. Git Workflow

* **Branch**: Poe works in `poe-dev` by default.
* **Validate** on every change:

  ```bash
  python3 scripts/validate_blocks.py blocks/**/*.json
  ```
* **Commit & Push**:

  ```bash
  ./scripts/poe_commit.sh "Add new <molt_type> block: <block_id>"
  ```

## 6. Tasks & TODOs

Poe should read this file, then look at `AI_TODO.json` (if present) for queued tasks:

```json
[
  { "task": "add block", "block_id": "user_auth", "category": "security", "molt_type": "Instruction" },
  { "task": "update schema", "file": "schemas/cantocore_block_schema.json" }
]
```

## 7. Contacts & Escalation

* When in doubt, log a warning to `logs/poe.log` and halt for human review.
