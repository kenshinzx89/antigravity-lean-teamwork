import os
import sys
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_stock_agi_integrity():
    """Verify that AGI on this computer is in its original (Stock) state without /teamwork-preview injected."""
    user_home = Path(os.path.expanduser("~"))
    stock_gemini_files = [
        user_home / ".gemini" / "config" / "GEMINI.md"
    ]
    for gf in stock_gemini_files:
        assert gf.exists(), f"Global file {gf} must exist"
        content = gf.read_text(encoding="utf-8")
        assert "Antigravity Global Operating Rules" in content, f"{gf} must be Antigravity Global Operating Rules"
        assert "/teamwork-preview" not in content or "Slash Command `/teamwork-preview` mặc định" in content, f"{gf} must NOT contain injected custom /teamwork-preview logic"
    print("[PASS] Stock AGI GEMINI.md on this machine is verified in clean original state.")

def test_project_skill_integrity():
    """Verify that Lean Teamwork is packaged independently as a clean custom skill in the project."""
    skill_file = REPO_ROOT / ".agents" / "skills" / "lean-teamwork" / "SKILL.md"
    assert skill_file.exists(), f"Skill file {skill_file} must exist"
    text = skill_file.read_text(encoding="utf-8")
    assert text.startswith("---"), "SKILL.md must start with YAML frontmatter"
    assert "name: lean-teamwork" in text, "SKILL.md must define name: lean-teamwork"
    assert "Iron Law of Verification" in text, "SKILL.md must enforce Iron Law of Verification"
    assert "Iron Law of Root Cause" in text, "SKILL.md must enforce Iron Law of Root Cause"
    assert "Ruling & Best-Path Fallback" in text, "SKILL.md must have Ruling & Best-Path Fallback"
    assert "Goal Confirmation Gate" in text, "SKILL.md must have Goal Confirmation Gate"
    assert "Continuous Self-Evolution" in text, "SKILL.md must have Continuous Self-Evolution"
    assert "First-Time Right Protocol" in text, "SKILL.md must enforce First-Time Right Protocol"
    assert "Anti-Survivorship Bias" in text, "SKILL.md must enforce Anti-Survivorship Bias"
    assert "Trajectory Churn Audit" in text, "SKILL.md must enforce Trajectory Churn Audit"
    assert "docs/learned_patterns.md" in text, "SKILL.md must link to project docs/learned_patterns.md"
    assert "C:/Users/MiTi" not in text, "SKILL.md must not contain hardcoded invalid user paths"
    print("[PASS] Lean Teamwork Project SKILL.md is verified.")

def test_evaluation_panel():
    """Verify Persistent Interactive Popup Gate (ask_question loop), Subagent Synthesizer, and Knowledge Segregation."""
    base = REPO_ROOT / ".agents" / "skills" / "lean-teamwork"

    # Template files must exist
    panel_template = base / "templates" / "evaluation_panel_template.md"
    assert panel_template.exists() and panel_template.stat().st_size > 0, \
        "evaluation_panel_template.md must exist and not be empty"

    # SKILL.md must enforce Persistent Popup Loop, ask_question, Subagent Synthesizer, and Knowledge Segregation
    skill_file = base / "SKILL.md"
    skill_text = skill_file.read_text(encoding="utf-8")
    assert "ask_question" in skill_text, "SKILL.md must mandate ask_question for popup modal"
    assert "Popup 2 Trạng Thái" in skill_text, "SKILL.md must enforce Two-State Popup"
    assert "Knowledge & Quota Synthesizer" in skill_text, "SKILL.md must specify subagent synthesizer role"
    assert "Nguyên Tắc Cách Ly Tri Thức" in skill_text, "SKILL.md must enforce Knowledge Segregation outside SKILL.md"

    print("[PASS] Persistent Interactive Popup Loop and Knowledge Segregation in SKILL.md are verified.")


def test_templates_and_references():
    """Verify all 6 templates and 4 reference docs exist with valid content."""
    base = REPO_ROOT / ".agents" / "skills" / "lean-teamwork"
    templates = [
        "execution_brief_template.md",
        "atomic_task_card_template.md",
        "compact_handoff_template.md",
        "cycle_reflection_template.md",
        "evaluation_panel_template.md",
        "evaluation_panel_template.html"
    ]
    references = [
        "architecture.md",
        "lean-protocol.md",
        "superpowers-integration.md",
        "systematic-debugging.md"
    ]
    for t in templates:
        p = base / "templates" / t
        assert p.exists() and p.stat().st_size > 0, f"Template {t} must exist and not be empty"
    for r in references:
        p = base / "references" / r
        assert p.exists() and p.stat().st_size > 0, f"Reference {r} must exist and not be empty"
    print("[PASS] All 6 templates and 4 references are verified.")

def test_learned_patterns_store():
    """Verify repository learned patterns store."""
    learned_md = REPO_ROOT / "docs" / "learned_patterns.md"
    assert learned_md.exists(), "docs/learned_patterns.md must exist in repository"
    content = learned_md.read_text(encoding="utf-8")
    assert "Learned Patterns" in content, "learned_patterns.md must have title"
    print("[PASS] Project docs/learned_patterns.md store is verified.")

def test_architecture_and_comparative_study():
    """Verify documentation separation and comparative study."""
    arch = REPO_ROOT / "docs" / "architecture.md"
    assert arch.exists(), "docs/architecture.md must exist"
    arch_content = arch.read_text(encoding="utf-8")
    assert "Stock Antigravity AGI" in arch_content, "Architecture must define Stock Antigravity AGI boundary"
    assert "Lean Teamwork Protocol" in arch_content, "Architecture must define Lean Teamwork Protocol"

    study = REPO_ROOT / "docs" / "ecosystem-comparative-study.md"
    assert study.exists(), "docs/ecosystem-comparative-study.md must exist"
    study_content = study.read_text(encoding="utf-8")
    assert "Hermes Agent" in study_content, "Must analyze Hermes Agent"
    assert "Ratchet Mechanism" in study_content, "Must analyze Ratchet Mechanism"
    assert "Golden Path" in study_content, "Must analyze Golden Path"
    print("[PASS] Architecture separation and comparative study docs are verified.")

def test_versioning_and_fast_sync():
    """Verify VERSION file, CHANGELOG.md, AGENTS.md guide, and sync_skill.py script exist and are valid."""
    # 1. VERSION file
    ver_file = REPO_ROOT / "VERSION"
    assert ver_file.exists() and ver_file.stat().st_size > 0, "VERSION file must exist"
    ver_text = ver_file.read_text(encoding="utf-8").strip()
    assert re.match(r"^\d+\.\d+\.\d+$", ver_text), f"VERSION {ver_text} must be valid SemVer (x.y.z)"

    # 2. CHANGELOG.md
    cl_file = REPO_ROOT / "CHANGELOG.md"
    assert cl_file.exists() and cl_file.stat().st_size > 0, "CHANGELOG.md must exist"

    # 3. AGENTS.md and GEMINI.md workspace controllers
    for ctrl_name in ["AGENTS.md", "GEMINI.md"]:
        ctrl_file = REPO_ROOT / ctrl_name
        assert ctrl_file.exists() and ctrl_file.stat().st_size > 0, f"{ctrl_name} workspace controller must exist"
        ctrl_content = ctrl_file.read_text(encoding="utf-8")
        assert "py sync_skill.py" in ctrl_content, f"{ctrl_name} must instruct to run py sync_skill.py"
        assert "Zero-Scan" in ctrl_content, f"{ctrl_name} must enforce Zero-Scan Protocol"

    # 4. sync_skill.py script and two-way smart sync
    sync_script = REPO_ROOT / "sync_skill.py"
    assert sync_script.exists() and sync_script.stat().st_size > 0, "sync_skill.py script must exist"
    sync_content = sync_script.read_text(encoding="utf-8")
    assert "auto_smart_sync" in sync_content, "sync_skill.py must contain auto_smart_sync"
    assert "sync_installed_to_source" in sync_content, "sync_skill.py must support PUSH (sync_installed_to_source)"
    assert "bidirectional_merge_patterns" in sync_content, "sync_skill.py must support bidirectional pattern merge"

    # 5. SKILL.md two-way sync enforcement
    skill_file = REPO_ROOT / ".agents" / "skills" / "lean-teamwork" / "SKILL.md"
    skill_content = skill_file.read_text(encoding="utf-8")
    assert "Two-Way Adaptive Sync" in skill_content, "SKILL.md must specify Two-Way Adaptive Sync"
    assert "🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡" in skill_content, "SKILL.md must specify Proposal Mode badge"
    assert "💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨" in skill_content, "SKILL.md must specify Acceptance Mode badge"

    print("[PASS] Versioning, CHANGELOG, AGENTS.md, GEMINI.md, and Two-Way Smart Sync are verified.")

def test_zero_touch_lifecycle_hooks():
    """Verify Zero-Touch PreInvocation lifecycle hooks for fully automatic operation without user commands."""
    hook_script = REPO_ROOT / "scripts" / "auto_sync_hook.py"
    assert hook_script.exists() and hook_script.stat().st_size > 0, "scripts/auto_sync_hook.py must exist"

    hooks_config = REPO_ROOT / ".agents" / "hooks.json"
    assert hooks_config.exists() and hooks_config.stat().st_size > 0, ".agents/hooks.json must exist"
    hooks_data = json.loads(hooks_config.read_text(encoding="utf-8"))
    assert "lean-teamwork-auto-sync" in hooks_data, "hooks.json must register lean-teamwork-auto-sync"
    assert "PreInvocation" in hooks_data["lean-teamwork-auto-sync"], "Must have PreInvocation hook"

    # Test executing workspace hook script
    import subprocess
    res = subprocess.run([sys.executable, str(hook_script)], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0, f"Hook execution failed: {res.stderr}"
    assert "injectSteps" in res.stdout, f"Hook output must injectSteps: {res.stdout}"
    assert "MANDATORY RE-ANCHOR" in res.stdout, "Hook output must contain MANDATORY RE-ANCHOR"
    assert "🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡" in res.stdout, "Workspace hook must contain Proposal Mode badge"
    assert "💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨" in res.stdout, "Workspace hook must contain Acceptance Mode badge"

    # Test global hook and script (~/.gemini/config/)
    user_home = Path(os.path.expanduser("~"))
    global_hook_json = user_home / ".gemini" / "config" / "hooks.json"
    global_hook_script = user_home / ".gemini" / "config" / "scripts" / "auto_reanchor_hook.py"
    assert global_hook_json.exists() and global_hook_json.stat().st_size > 0, "Global hooks.json must exist"
    assert global_hook_script.exists() and global_hook_script.stat().st_size > 0, "Global auto_reanchor_hook.py must exist"

    res_global = subprocess.run([sys.executable, str(global_hook_script)], capture_output=True, text=True, encoding="utf-8")
    assert res_global.returncode == 0, f"Global hook execution failed: {res_global.stderr}"
    assert "MANDATORY RE-ANCHOR" in res_global.stdout, "Global hook must inject MANDATORY RE-ANCHOR"
    assert "🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡" in res_global.stdout, "Global hook must contain Proposal Mode badge"
    assert "💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨" in res_global.stdout, "Global hook must contain Acceptance Mode badge"

    print("[PASS] Zero-Touch PreInvocation Lifecycle Hooks (Workspace & Global) are verified.")

def test_anti_survivorship_and_first_time_right():
    """Verify Anti-Survivorship Bias, Trajectory Churn Audit, and First-Time Right Protocol."""
    # 1. Check docs/self-evolution.md
    self_evo = REPO_ROOT / "docs" / "self-evolution.md"
    assert self_evo.exists(), "docs/self-evolution.md must exist"
    evo_text = self_evo.read_text(encoding="utf-8")
    assert "Anti-Survivorship Bias" in evo_text, "Must document Anti-Survivorship Bias"
    assert "Trajectory Churn Audit" in evo_text, "Must document Trajectory Churn Audit"
    assert "First-Time Right Protocol" in evo_text, "Must document First-Time Right Protocol"
    assert "Blind Lean" in evo_text, "Must address Blind Lean paradox"

    # 2. Check cycle_reflection_template.md
    cycle_tmpl = REPO_ROOT / ".agents" / "skills" / "lean-teamwork" / "templates" / "cycle_reflection_template.md"
    assert cycle_tmpl.exists(), "cycle_reflection_template.md must exist"
    cycle_text = cycle_tmpl.read_text(encoding="utf-8")
    assert "Turn Budget & Churn Analysis" in cycle_text, "cycle_reflection_template.md must audit turn budget and churn"

    print("[PASS] Anti-Survivorship Bias, Trajectory Churn Audit & First-Time Right Protocol are verified.")

def test_reflective_inquiry_and_knowledge_pruning():
    """Verify 5-Point Reflective Inquiry and Knowledge Pruning to prevent rule bloat and cognitive overload."""
    self_evo = REPO_ROOT / "docs" / "self-evolution.md"
    evo_text = self_evo.read_text(encoding="utf-8")
    assert "5-Point Reflective Inquiry" in evo_text, "Must document 5-Point Reflective Inquiry"
    assert "Knowledge Pruning" in evo_text, "Must document Knowledge Pruning"
    assert "Root Cause & Churn" in evo_text, "Must address Q1 Root Cause & Churn"
    assert "First-Time Right" in evo_text, "Must address Q2 First-Time Right"
    assert "Token Economy" in evo_text, "Must address Q3 Token Economy"
    assert "Velocity & Automation" in evo_text, "Must address Q4 Velocity & Automation"
    assert "Rule Pruning & Anti-Bloat" in evo_text, "Must address Q5 Rule Pruning & Anti-Bloat"

    skill_file = REPO_ROOT / ".agents" / "skills" / "lean-teamwork" / "SKILL.md"
    skill_text = skill_file.read_text(encoding="utf-8")
    assert "Bộ Khung Tự Vấn Phản Tư 5 Chiều" in skill_text, "SKILL.md must mandate 5-Point Reflective Inquiry"
    assert "Anti-Rule-Bloat" in skill_text, "SKILL.md must mandate Anti-Rule-Bloat"
    assert "Merge & Prune" in skill_text, "SKILL.md must enforce Merge & Prune"

    print("[PASS] 5-Point Reflective Inquiry and Knowledge Pruning (Anti-Rule-Bloat) are verified.")

if __name__ == "__main__":
    test_stock_agi_integrity()
    test_project_skill_integrity()
    test_evaluation_panel()
    test_templates_and_references()
    test_learned_patterns_store()
    test_architecture_and_comparative_study()
    test_versioning_and_fast_sync()
    test_zero_touch_lifecycle_hooks()
    test_anti_survivorship_and_first_time_right()
    test_reflective_inquiry_and_knowledge_pruning()
    print("\n============================================================")
    print("ALL 10/10 SYSTEM CHECKS PASSED SUCCESSFULLY (Exit Code 0).")
    print("Zero-Touch Auto Sync, Stock AGI, Lean Teamwork, Anti-Survivorship Bias & Anti-Rule-Bloat verified.")
    print("============================================================")
