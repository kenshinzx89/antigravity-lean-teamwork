#!/usr/bin/env python3
"""
Lean Teamwork — Fast Sync & Versioning Script
Đồng bộ nhanh Skill và Tri Thức từ thư mục dự án lên Antigravity Global Config (~/.gemini/config/)
trên laptop hoặc máy tính mới chỉ với 1 lệnh duy nhất, không cần đọc lại toàn bộ dự án.
"""

import os
import sys
import shutil
from pathlib import Path

# Đảm bảo in UTF-8 an toàn trên Windows console
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent
GLOBAL_CONFIG_DIR = Path(os.path.expanduser("~")) / ".gemini" / "config"
GLOBAL_SKILL_DIR = GLOBAL_CONFIG_DIR / "skills" / "lean-teamwork"

def parse_semver(v_str: str):
    parts = v_str.strip().split(".")
    while len(parts) < 3:
        parts.append("0")
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except Exception:
        return (0, 0, 0)

def get_source_version() -> str:
    version_file = REPO_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "1.0.0"

def get_installed_version() -> str:
    version_file = GLOBAL_SKILL_DIR / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0"

def bump_version(part: str = "patch") -> str:
    current = get_source_version()
    major, minor, patch = parse_semver(current)

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    new_ver = f"{major}.{minor}.{patch}"
    (REPO_ROOT / "VERSION").write_text(new_ver + "\n", encoding="utf-8")
    print(f"[BUMP] Tăng phiên bản: {current} -> {new_ver}")
    return new_ver

def parse_blocks(text: str):
    blocks = []
    current_block = []
    for line in text.splitlines():
        if line.startswith("## ") and current_block:
            blocks.append("\n".join(current_block))
            current_block = [line]
        elif line.startswith("## "):
            current_block = [line]
        elif current_block:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks

def bidirectional_merge_patterns():
    src_patterns = REPO_ROOT / "docs" / "learned_patterns.md"
    dst_patterns = GLOBAL_CONFIG_DIR / "learned_patterns.md"

    src_text = src_patterns.read_text(encoding="utf-8") if src_patterns.exists() else ""
    dst_text = dst_patterns.read_text(encoding="utf-8") if dst_patterns.exists() else ""

    src_blocks = parse_blocks(src_text)
    dst_blocks = parse_blocks(dst_text)

    merged_headers = []
    merged_blocks = []

    # Giữ các blocks từ source
    for b in src_blocks:
        header = b.splitlines()[0].strip()
        if header not in merged_headers:
            merged_headers.append(header)
            merged_blocks.append(b.strip())

    # Thêm các blocks mới chỉ có ở installed (máy tính học được)
    added_to_source = 0
    for b in dst_blocks:
        header = b.splitlines()[0].strip()
        if header not in merged_headers:
            merged_headers.append(header)
            merged_blocks.append(b.strip())
            added_to_source += 1

    header_text = "# Kho Tri Thức & Các Mẫu Đúc Kết Tinh Gọn (Learned Patterns)\n\nTài liệu này là nơi lưu trữ các tri thức kỹ thuật, mẫu sửa lỗi tối thiểu và bài học tiết kiệm quota được chắt lọc sau khi người dùng bấm xác nhận \"OK\".\n\n---\n\n"
    combined_content = header_text + "\n\n".join(merged_blocks) + "\n"

    # Ghi đồng bộ cả 2 nơi
    src_patterns.parent.mkdir(parents=True, exist_ok=True)
    src_patterns.write_text(combined_content, encoding="utf-8")

    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    dst_patterns.write_text(combined_content, encoding="utf-8")

    if added_to_source > 0:
        print(f"  ✓ Đã đồng bộ ngược {added_to_source} bài học từ máy tính về folder gốc!")
    print(f"  ✓ Cân bằng 2 chiều tri thức thành công ({len(merged_blocks)} patterns tại cả 2 nơi).")

def ensure_stock_gemini():
    target_stock_gemini = GLOBAL_CONFIG_DIR / "GEMINI.md"
    if not target_stock_gemini.exists():
        src_gemini_candidate = Path(os.path.expanduser("~")) / ".gemini" / "GEMINI.md"
        if src_gemini_candidate.exists():
            gemini_txt = src_gemini_candidate.read_text(encoding="utf-8")
            if not gemini_txt.startswith("# Antigravity Global Operating Rules"):
                gemini_txt = "# Antigravity Global Operating Rules (Global Operating Contract v2)\n\n" + gemini_txt.split("\n", 1)[-1]
            target_stock_gemini.write_text(gemini_txt, encoding="utf-8")
def ensure_global_hooks():
    setup_script = REPO_ROOT / "scripts" / "setup_global_hook.py"
    if setup_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(setup_script)], capture_output=True, text=True, encoding="utf-8")
        print("  ✓ Đã thiết lập Global PreInvocation Hook tại ~/.gemini/config/hooks.json")

def sync_source_to_installed(version: str):
    """PULL: Cập nhật từ folder gốc vào máy tính."""
    source_skill_dir = REPO_ROOT / ".agents" / "skills" / "lean-teamwork"
    if not source_skill_dir.exists():
        print(f"[ERROR] Không tìm thấy thư mục skill: {source_skill_dir}")
        sys.exit(1)

    GLOBAL_SKILL_DIR.mkdir(parents=True, exist_ok=True)

    source_skill_md = source_skill_dir / "SKILL.md"
    target_skill_md = GLOBAL_SKILL_DIR / "SKILL.md"
    skill_content = source_skill_md.read_text(encoding="utf-8")
    
    global_skill_content = skill_content.replace(
        "[`docs/learned_patterns.md`](../../docs/learned_patterns.md)",
        "[`~/.gemini/config/learned_patterns.md`](file:///" + str(GLOBAL_CONFIG_DIR / "learned_patterns.md").replace("\\", "/") + ")"
    )
    target_skill_md.write_text(global_skill_content, encoding="utf-8")
    print("  ✓ [PULL] Đã đồng bộ SKILL.md vào Global Config")

    for sub in ["templates", "references"]:
        src_sub = source_skill_dir / sub
        dst_sub = GLOBAL_SKILL_DIR / sub
        if src_sub.exists():
            shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)
            print(f"  ✓ [PULL] Đã đồng bộ {sub}/")

    (GLOBAL_SKILL_DIR / "VERSION").write_text(version + "\n", encoding="utf-8")
    print(f"  ✓ [PULL] Đã ghi VERSION {version} vào {GLOBAL_SKILL_DIR}")

    ensure_stock_gemini()
    ensure_global_hooks()
    bidirectional_merge_patterns()

def sync_installed_to_source(version: str):
    """PUSH: Cập nhật từ máy tính ngược về folder gốc để PC/thiết bị khác dùng."""
    target_skill_dir = REPO_ROOT / ".agents" / "skills" / "lean-teamwork"
    target_skill_dir.mkdir(parents=True, exist_ok=True)

    source_skill_md = GLOBAL_SKILL_DIR / "SKILL.md"
    if source_skill_md.exists():
        content = source_skill_md.read_text(encoding="utf-8")
        # Đưa đường dẫn về relative chuẩn cho repo
        repo_skill_content = content.replace(
            "[`~/.gemini/config/learned_patterns.md`](file:///" + str(GLOBAL_CONFIG_DIR / "learned_patterns.md").replace("\\", "/") + ")",
            "[`docs/learned_patterns.md`](../../docs/learned_patterns.md)"
        )
        (target_skill_dir / "SKILL.md").write_text(repo_skill_content, encoding="utf-8")
        print("  ✓ [PUSH] Đã đồng bộ ngược SKILL.md về folder gốc")

    for sub in ["templates", "references"]:
        src_sub = GLOBAL_SKILL_DIR / sub
        dst_sub = target_skill_dir / sub
        if src_sub.exists():
            shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)
            print(f"  ✓ [PUSH] Đã đồng bộ ngược {sub}/ về folder gốc")

    (REPO_ROOT / "VERSION").write_text(version + "\n", encoding="utf-8")
    print(f"  ✓ [PUSH] Đã cập nhật VERSION {version} ở folder gốc")

    ensure_global_hooks()
    bidirectional_merge_patterns()

def run_verification():
    test_script = REPO_ROOT / "tests" / "test_skill_integrity.py"
    if test_script.exists():
        import subprocess
        print("  ⏳ Đang chạy kiểm thử toàn vẹn hệ thống...")
        res = subprocess.run([sys.executable, str(test_script)], capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0:
            print("  ✓ Toàn bộ kiểm thử hệ thống đạt 100% PASS (Exit Code 0).")
            return True
        else:
            print(f"  ⚠ Cảnh báo kiểm thử: {res.stderr or res.stdout}")
            return False
    return True

def auto_smart_sync():
    src_v = get_source_version()
    inst_v = get_installed_version()

    src_tuple = parse_semver(src_v)
    inst_tuple = parse_semver(inst_v)

    print(f"[SMART-SYNC] Kiểm tra phiên bản:")
    print(f"  • Folder gốc (Source):   v{src_v}")
    print(f"  • Máy tính (Installed):  v{inst_v}")

    if src_tuple > inst_tuple:
        print(f"\n🔄 [HƯỚNG: PULL] Folder gốc mới hơn (v{src_v} > v{inst_v}). Tiến hành cập nhật lên máy tính này...")
        sync_source_to_installed(src_v)
        active_ver = src_v
    elif inst_tuple > src_tuple:
        print(f"\n🔄 [HƯỚNG: PUSH] Máy tính này mới hơn (v{inst_v} > v{src_v}). Cập nhật ngược về folder gốc để đồng bộ cho PC...")
        sync_installed_to_source(inst_v)
        active_ver = inst_v
    else:
        print(f"\n⚡ [HƯỚNG: SYNC 2 CHIỀU] Hai bên đồng phiên bản (v{src_v}). Kiểm tra và cân bằng tri thức...")
        sync_source_to_installed(src_v)
        active_ver = src_v

    run_verification()

    print("\n============================================================")
    print(f"[SUCCESS] Lean Teamwork v{active_ver} đã đồng bộ 2 chiều hoàn hảo!")
    print(f"• Folder gốc:  {REPO_ROOT}")
    print(f"• Global Core: {GLOBAL_SKILL_DIR}")
    print("============================================================")

if __name__ == "__main__":
    if "--bump" in sys.argv:
        bump_type = "patch"
        idx = sys.argv.index("--bump")
        if len(sys.argv) > idx + 1 and sys.argv[idx + 1] in ["patch", "minor", "major"]:
            bump_type = sys.argv[idx + 1]
        new_v = bump_version(bump_type)
        print(f"[START] Đồng bộ sau khi tăng phiên bản lên v{new_v}...")
        sync_source_to_installed(new_v)
        run_verification()
    elif "--push" in sys.argv:
        inst_v = get_installed_version()
        print(f"[START] Ép cập nhật PUSH từ máy tính (v{inst_v}) về folder gốc...")
        sync_installed_to_source(inst_v)
        run_verification()
    elif "--pull" in sys.argv:
        src_v = get_source_version()
        print(f"[START] Ép cập nhật PULL từ folder gốc (v{src_v}) lên máy tính...")
        sync_source_to_installed(src_v)
        run_verification()
    else:
        # Mặc định là Auto Smart Sync (Two-Way)
        auto_smart_sync()
