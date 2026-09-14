# -*- coding: utf-8 -*-
"""
Antigravity Skill Manager & Context Pruner
Công cụ kiểm toán, tắt bớt skill không dùng sau 3-4 chu kỳ nghiệm thu để tiết kiệm Context Window,
đồng thời cho phép gọi lại (restore) tức thì bất cứ khi nào cần.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Set

# Đảm bảo in UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

GLOBAL_CONFIG_DIR = Path.home() / ".gemini" / "config"
SKILLS_DIR = GLOBAL_CONFIG_DIR / "skills"
ARCHIVE_DIR = GLOBAL_CONFIG_DIR / "skills_archive"

# Các skill nòng cốt KHÔNG BAO GIỜ ĐƯỢC TẮT
PROTECTED_SKILLS = {
    "lean-teamwork",
    "agentic-engineering",
    "ai-first-engineering",
    "agent-harness-construction",
    "context-engineering",
    "git-workflow",
    "systematic-debugging"
}


def get_active_skills() -> List[str]:
    """Lấy danh sách các skill đang hoạt động."""
    if not SKILLS_DIR.exists():
        return []
    return sorted([d.name for d in SKILLS_DIR.iterdir() if d.is_dir()])


def get_archived_skills() -> List[str]:
    """Lấy danh sách các skill đang được cất gọn (archive)."""
    if not ARCHIVE_DIR.exists():
        return []
    return sorted([d.name for d in ARCHIVE_DIR.iterdir() if d.is_dir()])


def archive_skill(skill_name: str) -> bool:
    """Tắt một skill bằng cách di chuyển vào skills_archive để giải phóng context."""
    if skill_name in PROTECTED_SKILLS:
        print(f"  [BẢO VỆ] Skill '{skill_name}' là kỹ năng nòng cốt, không thể tắt.")
        return False

    src = SKILLS_DIR / skill_name
    if not src.exists():
        return False

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    dst = ARCHIVE_DIR / skill_name

    # Di chuyển an toàn
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    return True


def restore_skill(skill_name: str) -> bool:
    """Bật lại một skill từ skills_archive trở về skills hoạt động."""
    src = ARCHIVE_DIR / skill_name
    if not src.exists():
        print(f"  [LỖI] Không tìm thấy skill '{skill_name}' trong thư mục cất gọn.")
        return False

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    dst = SKILLS_DIR / skill_name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    print(f"  ✓ Đã bật lại skill '{skill_name}' thành công! Sẵn sàng sử dụng 100%.")
    return True


def audit_irrelevant_skills_for_repo(repo_path: Path) -> List[Tuple[str, str]]:
    """
    Rà soát các skill không thuộc tech-stack của dự án hiện tại để đề xuất tắt bớt.
    Ví dụ: Dự án Python/Win32 không cần django, laravel, quarkus, blender, fsharp, v.v.
    """
    active = get_active_skills()
    candidates_to_prune = []

    stacks_to_check = {
        "laravel": "Dự án hiện tại không sử dụng PHP / Laravel framework",
        "django": "Dự án hiện tại không sử dụng Python Django / Celery",
        "quarkus": "Dự án hiện tại không sử dụng Java / Quarkus framework",
        "springboot": "Dự án hiện tại không sử dụng Java / Spring Boot",
        "fsharp": "Dự án hiện tại không sử dụng F# / .NET",
        "csharp": "Dự án hiện tại không sử dụng C# / .NET",
        "dotnet": "Dự án hiện tại không sử dụng .NET runtime",
        "perl": "Dự án hiện tại không sử dụng Perl",
        "blender": "Dự án hiện tại không sử dụng Blender 3D animation",
        "bigquery": "Dự án hiện tại không sử dụng Google Cloud BigQuery",
        "clickhouse": "Dự án hiện tại không sử dụng ClickHouse OLAP",
        "cisco": "Dự án hiện tại không sử dụng Cisco IOS networking",
        "visa-doc": "Dự án hiện tại không sử dụng xử lý hồ sơ Visa",
        "healthcare": "Dự án hiện tại không sử dụng chuẩn Y tế / HIPAA / PHI",
        "homelab": "Dự án hiện tại không cấu hình mạng Homelab / VLAN",
    }

    for skill in active:
        if skill in PROTECTED_SKILLS:
            continue
        for key, reason in stacks_to_check.items():
            if key in skill.lower():
                candidates_to_prune.append((skill, reason))
                break

    return candidates_to_prune


def prune_unneeded_skills(repo_path: Path, dry_run: bool = False) -> List[Tuple[str, str]]:
    """Thực hiện tắt các skill không dùng để tiết kiệm context."""
    candidates = audit_irrelevant_skills_for_repo(repo_path)
    pruned = []

    for skill, reason in candidates:
        if dry_run:
            pruned.append((skill, reason))
        else:
            if archive_skill(skill):
                pruned.append((skill, reason))

    return pruned


# ==============================================================================
# BẢNG ÁNH XẠ DỰ PHÓNG KỸ NĂNG ĐÓN ĐẦU (PREDICTIVE SKILL ROUTING TABLE)
# ==============================================================================
PREDICTIVE_ROUTING_TABLE = {
    "ui_core": {
        "title": "Hoàn tất Core UI / Thuật toán tương tác",
        "description": "Vừa hoàn thành giao diện cơ bản, bố cục hoặc logic thuật toán người dùng.",
        "predicted_scenarios": [
            "1. Thêm hiệu ứng âm thanh & hoạt họa tương tác (motion-ui, frontend-ui-engineering)",
            "2. Đóng gói PWA / Tối ưu giao diện cảm ứng di động (shipping-and-launch, vite-patterns)",
            "3. Mở rộng tính năng đố vui / Gamification (lean-teamwork)"
        ],
        "unload_candidates": [
            "playwright-testing", "e2e-testing", "browser-qa", "a11y-debugging"
        ],
        "preload_candidates": [
            "motion-ui", "frontend-ui-engineering", "shipping-and-launch", "vite-patterns"
        ]
    },
    "backend_api": {
        "title": "Hoàn tất Backend API / Dịch vụ dữ liệu",
        "description": "Vừa hoàn thành các endpoint API, lược đồ database hoặc logic backend.",
        "predicted_scenarios": [
            "1. Tích hợp Frontend kết nối API (frontend-patterns, api-connector-builder)",
            "2. Chuẩn hóa Hợp đồng API & Tài liệu (contract-first, api-design)",
            "3. Rà soát bảo mật & Giới hạn tần suất gọi API (security-review)"
        ],
        "unload_candidates": [
            "database-migrations", "backend-patterns", "mysql-patterns", "postgres-patterns"
        ],
        "preload_candidates": [
            "api-connector-builder", "contract-first", "frontend-patterns", "security-review"
        ]
    },
    "mvp_done": {
        "title": "Hoàn tất phiên bản MVP toàn diện",
        "description": "Toàn bộ tính năng cốt lõi của ứng dụng đã chạy mượt mà và kiểm thử đạt 100%.",
        "predicted_scenarios": [
            "1. Tối ưu kích thước bundle & Hiệu năng tải trang (performance-optimization, vite-patterns)",
            "2. Đóng gói phát hành & Tự động hóa CI/CD (shipping-and-launch, ci-cd-and-automation)",
            "3. Tối ưu tìm kiếm & Kiểm toán SEO (seo, production-audit)"
        ],
        "unload_candidates": [
            "tdd-workflow", "systematic-debugging", "exploratory-dev"
        ],
        "preload_candidates": [
            "shipping-and-launch", "performance-optimization", "ci-cd-and-automation", "seo"
        ]
    },
    "bugfix_complete": {
        "title": "Hoàn tất Sửa lỗi & Đạt chuẩn Green",
        "description": "Đã giải quyết dứt điểm nguyên nhân gốc và kiểm thử hồi quy pass 100%.",
        "predicted_scenarios": [
            "1. Đo kiểm hiệu năng & Điểm chuẩn sức khỏe mã nguồn (benchmark, codehealth-mcp)",
            "2. Tiếp tục phát triển các tính năng nghiệp vụ kế tiếp"
        ],
        "unload_candidates": [
            "systematic-debugging", "troubleshooting"
        ],
        "preload_candidates": [
            "benchmark", "codehealth-mcp"
        ]
    }
}


def predict_next_skills(domain_key: str) -> Dict:
    """
    Dự phóng nhu cầu lượt kế tiếp và các kỹ năng cần dọn dẹp / nạp đón đầu.
    """
    domain = domain_key.lower().strip()
    if domain not in PREDICTIVE_ROUTING_TABLE:
        # Tìm kiếm mờ nếu không khớp trực tiếp
        matched_key = None
        for k in PREDICTIVE_ROUTING_TABLE:
            if k in domain or domain in k:
                matched_key = k
                break
        if not matched_key:
            return {
                "error": f"Không tìm thấy domain '{domain_key}'. Các domain hợp lệ: {list(PREDICTIVE_ROUTING_TABLE.keys())}",
                "valid_domains": list(PREDICTIVE_ROUTING_TABLE.keys())
            }
        domain = matched_key

    info = PREDICTIVE_ROUTING_TABLE[domain]
    return {
        "domain": domain,
        "title": info["title"],
        "description": info["description"],
        "predicted_scenarios": info["predicted_scenarios"],
        "unload_candidates": info["unload_candidates"],
        "preload_candidates": info["preload_candidates"]
    }


def switch_skills(unload_skills: List[str], load_skills: List[str]) -> Dict[str, List[str]]:
    """
    Thực hiện chuyển giao kỹ năng động (Dynamic Skill Switch):
    - Cất (archive) các kỹ năng kiểm thử/nặng không còn dùng để giải phóng Context.
    - Bật lại (restore) các kỹ năng mới chuẩn bị cho pha kế tiếp.
    """
    unloaded_success = []
    loaded_success = []

    for s in unload_skills:
        s_clean = s.strip()
        if not s_clean:
            continue
        if archive_skill(s_clean):
            unloaded_success.append(s_clean)

    for s in load_skills:
        s_clean = s.strip()
        if not s_clean:
            continue
        if restore_skill(s_clean):
            loaded_success.append(s_clean)

    return {
        "unloaded": unloaded_success,
        "loaded": loaded_success
    }


def print_status():
    active = get_active_skills()
    archived = get_archived_skills()
    print("============================================================")
    print("📊 TRẠNG THÁI KỸ NĂNG ANTIGRAVITY (SKILL CONTEXT MONITOR)")
    print("============================================================")
    print(f"• Đang hoạt động (Active): {len(active)} skills (nạp vào context mỗi lượt)")
    print(f"• Đang cất gọn (Archived): {len(archived)} skills (giải phóng context)")
    print("============================================================")


if __name__ == "__main__":
    REPO_ROOT = Path(__file__).resolve().parent.parent

    if "--list" in sys.argv:
        print_status()
    elif "--restore" in sys.argv:
        idx = sys.argv.index("--restore")
        if len(sys.argv) > idx + 1:
            target = sys.argv[idx + 1]
            restore_skill(target)
        else:
            print("Cần cung cấp tên skill: --restore <skill_name>")
    elif "--restore-all" in sys.argv:
        archived = get_archived_skills()
        for s in archived:
            restore_skill(s)
        print(f"✓ Đã khôi phục toàn bộ {len(archived)} skills về active.")
    elif "--audit" in sys.argv:
        candidates = audit_irrelevant_skills_for_repo(REPO_ROOT)
        print_status()
        print(f"\n🔍 Phát hiện {len(candidates)} skills không thuộc tech-stack hiện tại:")
        for s, r in candidates[:20]:
            print(f"  • {s}: {r}")
        if len(candidates) > 20:
            print(f"  ... và {len(candidates) - 20} skills khác.")
    elif "--prune" in sys.argv:
        pruned = prune_unneeded_skills(REPO_ROOT, dry_run=False)
        print_status()
        print(f"\n✂️ ĐÃ TẮT BỚT {len(pruned)} SKILLS ĐỂ TIẾT KIỆM CONTEXT:")
        for s, r in pruned[:15]:
            print(f"  ✓ Đã cất '{s}' -> {r}")
        if len(pruned) > 15:
            print(f"  ... và {len(pruned) - 15} skills khác.")
        print("\n💡 Ghi chú: Khi cần dùng lại bất kỳ skill nào, chỉ cần chạy:")
        print("   py scripts/manage_skills.py --restore <tên_skill>")
        print("   hoặc bảo AI: 'Bật lại skill [tên_skill]' là xong!")
    elif "--predict" in sys.argv:
        idx = sys.argv.index("--predict")
        domain = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else "ui_core"
        prediction = predict_next_skills(domain)
        if "error" in prediction:
            print(f"❌ {prediction['error']}")
        else:
            print("============================================================")
            print(f"🧭 DỰ PHÓNG NHU CẦU & KỸ NĂNG KẾ TIẾP: [{prediction['title']}]")
            print("============================================================")
            print(f"Mô tả: {prediction['description']}")
            print("\n🔮 Kịch bản tiếp theo logic tự nhiên:")
            for sc in prediction["predicted_scenarios"]:
                print(f"  {sc}")
            print("\n🧹 Kỹ năng đề xuất cất gọn (Unload để giải phóng Context):")
            for u in prediction["unload_candidates"]:
                print(f"  - {u}")
            print("\n🚀 Kỹ năng đề xuất nạp đón đầu (Preload cho lượt mới):")
            for p in prediction["preload_candidates"]:
                print(f"  + {p}")
            print("============================================================")
    elif "--switch" in sys.argv:
        unload_list = []
        load_list = []
        if "--unload" in sys.argv:
            u_idx = sys.argv.index("--unload")
            if len(sys.argv) > u_idx + 1:
                unload_list = [s.strip() for s in sys.argv[u_idx + 1].split(",")]
        if "--load" in sys.argv:
            l_idx = sys.argv.index("--load")
            if len(sys.argv) > l_idx + 1:
                load_list = [s.strip() for s in sys.argv[l_idx + 1].split(",")]
        res = switch_skills(unload_list, load_list)
        print("🔄 KẾT QUẢ CHUYỂN GIAO KỸ NĂNG ĐỘNG (DYNAMIC SKILL SWITCH):")
        print(f"  • Đã cất (Unloaded): {res['unloaded']}")
        print(f"  • Đã nạp (Loaded): {res['loaded']}")
    else:
        print_status()
        print("\nCách dùng:")
        print("  py scripts/manage_skills.py --list                 # Xem số lượng active / archived")
        print("  py scripts/manage_skills.py --audit                # Quét các skill không dùng")
        print("  py scripts/manage_skills.py --prune                # Tắt bớt skill để tiết kiệm context")
        print("  py scripts/manage_skills.py --restore <ten>        # Khôi phục 1 skill")
        print("  py scripts/manage_skills.py --restore-all          # Khôi phục toàn bộ")
        print("  py scripts/manage_skills.py --predict <domain>    # Dự phóng nhu cầu & kỹ năng kế tiếp")
        print("  py scripts/manage_skills.py --switch --unload <a,b> --load <c,d> # Chuyển giao động")
