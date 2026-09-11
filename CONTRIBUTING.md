# Contributing to Lean Teamwork

Thank you for your interest in contributing to **Lean Teamwork**!

Lean Teamwork is an ultra-lean, context-disciplined, token-efficient multi-agent orchestration framework for Antigravity, Claude Code, and autonomous developer agents.

---

## 🧭 Core Engineering Principles

Before submitting a Pull Request, ensure your contributions adhere to our immutable design tenets:

1. **Zero-Scan Protocol**:
   - Never perform unbounded recursive scans or dump hundreds of repository files into agent context.
   - Operations must resolve through targeted scripts (`sync_skill.py`) or precise path anchors.

2. **First-Time Right Protocol (Anti-Survivorship Bias)**:
   - Always **Inspect First** (read authoritative specs/APIs) before proposing edits.
   - Avoid "Blind Lean" (blind guessing under the false premise of saving tokens) which triggers 5–10 iterative churn turns.

3. **Knowledge Segregation**:
   - `SKILL.md` is strictly reserved for orchestration rules (<150 lines).
   - Knowledge patterns, heuristics, and domain learnings belong in `docs/learned_patterns.md` only.

4. **5-Point Reflective Inquiry & Anti-Rule-Bloat**:
   - Never append redundant rules that bloat token windows and cause cognitive overload.
   - Always consolidate related patterns (Merge & Generalize) or prune obsolete guidelines.

5. **Evidence-Matched Verification (Exit Code 0)**:
   - Every change must pass `python tests/test_skill_integrity.py` with 100% PASS before merge.

---

## 🛠️ Development & Testing Workflow

```bash
# 1. Clone repository
git clone https://github.com/your-username/antigravity-lean-teamwork.git
cd antigravity-lean-teamwork

# 2. Run two-way adaptive sync & test suite
python sync_skill.py

# 3. Run integrity tests directly
python tests/test_skill_integrity.py
```

---

## 📦 Pull Request Checklist

- [ ] All 10/10 system integrity checks pass (`python tests/test_skill_integrity.py`).
- [ ] No personal or machine-specific absolute paths are hardcoded.
- [ ] `SKILL.md` remains lean and under 150 lines.
- [ ] Version and `CHANGELOG.md` updated if introducing new features.
