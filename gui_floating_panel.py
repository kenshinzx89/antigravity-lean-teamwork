import os
import sys
import json
import tkinter as tk
from tkinter import font

def create_floating_panel(task_name="Nhiệm Vụ Hiện Tại", checks=None, status_file=None):
    if checks is None:
        checks = [
            ("Template Bảng Đánh Giá", "Đã tạo template tại .agents/skills/lean-teamwork/"),
            ("Quy trình Persistent Side Panel", "Mục 4.5 trong SKILL.md đã cấu hình"),
            ("Subagent Tổng Hợp & Tri Thức Ngoài", "Kinh nghiệm lưu ra file ngoài, không nạp vào SKILL.md"),
            ("Kiểm thử tự động hệ thống", "py tests/test_skill_integrity.py -> 6/6 PASS")
        ]

    root = tk.Tk()
    root.title("📋 Bảng Đánh Giá Độc Lập — Lean Teamwork")
    
    # Kích thước và vị trí góc trên-phải màn hình
    w, h = 480, 560
    sw = root.winfo_screenwidth()
    x = sw - w - 30
    y = 60
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.configure(bg="#0f172a")
    
    # Luôn nổi trên cùng (TopMost) nhưng không chiếm quyền điều khiển (non-modal)
    root.attributes("-topmost", True)

    # Header Frame
    header = tk.Frame(root, bg="#1e293b", padx=16, pady=12)
    header.pack(fill="x", padx=12, pady=(12, 6))

    tag_frame = tk.Frame(header, bg="#1e293b")
    tag_frame.pack(fill="x")

    badge = tk.Label(tag_frame, text="● CỬA SỔ NỔI ĐỘC LẬP", font=("Segoe UI", 8, "bold"), fg="#10b981", bg="#064e3b", padx=6, pady=2)
    badge.pack(side="left")

    status_lbl = tk.Label(tag_frame, text="⏳ Chờ Kiểm Thử", font=("Segoe UI", 9, "bold"), fg="#fbbf24", bg="#1e293b")
    status_lbl.pack(side="right")

    title_lbl = tk.Label(header, text=f"📋 {task_name}", font=("Segoe UI", 12, "bold"), fg="#f8fafc", bg="#1e293b", anchor="w")
    title_lbl.pack(fill="x", pady=(6, 2))

    sub_lbl = tk.Label(header, text="Cửa sổ này luôn nổi độc lập. Bạn vẫn chat bên IDE bình thường.", font=("Segoe UI", 8), fg="#94a3b8", bg="#1e293b", anchor="w")
    sub_lbl.pack(fill="x")

    # Checklist Frame
    list_frame = tk.Frame(root, bg="#0f172a", padx=12, pady=6)
    list_frame.pack(fill="both", expand=True)

    sec_lbl = tk.Label(list_frame, text="CHECKLIST KIỂM TRA (Tự Test Trên Máy):", font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#0f172a", anchor="w")
    sec_lbl.pack(fill="x", pady=(0, 6))

    check_vars = []
    for idx, (title, desc) in enumerate(checks, 1):
        item_card = tk.Frame(list_frame, bg="#1e293b", padx=10, pady=8, highlightbackground="#334155", highlightthickness=1)
        item_card.pack(fill="x", pady=4)

        var = tk.BooleanVar(value=True)
        check_vars.append(var)

        cb = tk.Checkbutton(item_card, text=f"{idx}. {title}", variable=var, font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#1e293b", activebackground="#1e293b", activeforeground="#38bdf8", selectcolor="#0f172a", cursor="hand2")
        cb.pack(anchor="w")

        d_lbl = tk.Label(item_card, text=desc, font=("Segoe UI", 8), fg="#94a3b8", bg="#1e293b", anchor="w")
        d_lbl.pack(anchor="w", padx=(24, 0))

    # Hướng dẫn
    guide_frame = tk.Frame(root, bg="#1e293b", padx=12, pady=8, highlightbackground="#334155", highlightthickness=1)
    guide_frame.pack(fill="x", padx=12, pady=4)

    g_title = tk.Label(guide_frame, text="💬 Chưa ưng ý? Chat tiếp ở IDE để tôi sửa.", font=("Segoe UI", 8, "bold"), fg="#f59e0b", bg="#1e293b", anchor="w")
    g_title.pack(fill="x")
    g_desc = tk.Label(guide_frame, text="Cửa sổ này sẽ giữ nguyên cho đến khi bạn xác nhận hoàn thành.", font=("Segoe UI", 8), fg="#94a3b8", bg="#1e293b", anchor="w")
    g_desc.pack(fill="x")

    # Action Buttons
    action_frame = tk.Frame(root, bg="#0f172a", padx=12, pady=10)
    action_frame.pack(fill="x")

    def on_confirm():
        if status_file:
            try:
                with open(status_file, "w", encoding="utf-8") as f:
                    json.dump({"status": "COMPLETED", "task": task_name}, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
        btn_confirm.configure(text="✅ ĐÃ XÁC NHẬN HOÀN THÀNH!", bg="#059669")
        root.after(1000, root.destroy)

    btn_confirm = tk.Button(
        action_frame,
        text="✅ ĐÃ KIỂM TRA XONG — XÁC NHẬN HOÀN THÀNH",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",
        bg="#10b981",
        activebackground="#059669",
        activeforeground="#ffffff",
        padx=12,
        pady=10,
        relief="flat",
        cursor="hand2",
        command=on_confirm
    )
    btn_confirm.pack(fill="x")

    root.mainloop()

if __name__ == "__main__":
    task = "Phương Án 1: Persistent Side Panel Gate"
    if len(sys.argv) > 1:
        task = sys.argv[1]
    create_floating_panel(task_name=task)
