# -*- coding: utf-8 -*-
"""
Kiểm thử Toàn diện Cầu nối 2 Chiều Lean Teamwork <-> Antigravity Desktop Widget
"""

import sys
import os
import json
import time
import unittest
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
WIDGET_ROOT = REPO_ROOT / "widget" if (REPO_ROOT / "widget").exists() else Path(r"c:\Users\tient\Desktop\Du An\AntigravityWidget")

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(WIDGET_ROOT))

import teamwork_bridge
from core.teamwork_service import get_teamwork_service
from core.layout import horizontal_layout, calculate_account_chip_width
from core import antigravity_service


class TestTeamworkWidgetIntegration(unittest.TestCase):

    def setUp(self):
        teamwork_bridge.clear_bridge()

    def tearDown(self):
        teamwork_bridge.clear_bridge()

    def test_01_bridge_proposal_lifecycle(self):
        """Test phát đề xuất kế hoạch và đọc lại từ TeamworkService."""
        options = [
            {"id": 1, "text": "Phương án 1 (Recommended)", "recommended": True},
            {"id": 2, "text": "Phương án 2", "recommended": False}
        ]
        ok = teamwork_bridge.publish_proposal("Tích hợp Widget", options, duration_seconds=150)
        self.assertTrue(ok)

        tw_service = get_teamwork_service()
        display = tw_service.get_display_info()

        self.assertTrue(display["active"])
        self.assertEqual(display["status"], "PROPOSAL")
        self.assertIn("🧭", display["label"])
        self.assertEqual(len(display["options"]), 2)
        self.assertGreater(display["remaining_seconds"], 140)

    def test_02_widget_click_roundtrip(self):
        """Test người dùng click chọn phương án trên Widget và IDE nhận được phản hồi."""
        options = [{"id": 1, "text": "Phương án 1", "recommended": True}]
        teamwork_bridge.publish_proposal("Test Click", options, duration_seconds=150)

        tw_service = get_teamwork_service()
        # Mô phỏng click từ widget popover
        tw_service.submit_response("SELECT_OPTION", option_id=1)

        # Kiểm tra IDE đọc được response
        resp = teamwork_bridge.check_user_response(mark_handled=True)
        self.assertIsNotNone(resp)
        self.assertEqual(resp["action"], "SELECT_OPTION")
        self.assertEqual(resp["selected_option_id"], 1)

        # Lần 2 đã handled nên trả về None
        resp_again = teamwork_bridge.check_user_response()
        self.assertIsNone(resp_again)

    def test_03_acceptance_lifecycle(self):
        """Test phát tín hiệu nghiệm thu và người dùng bấm duyệt."""
        ok = teamwork_bridge.publish_acceptance(
            title="Nghiệm thu Widget Bridge",
            summary="Đã hoàn thành xuất sắc toàn bộ tính năng",
            files_changed=["core/teamwork_service.py", "core/layout.py"],
            exit_code=0
        )
        self.assertTrue(ok)

        tw_service = get_teamwork_service()
        display = tw_service.get_display_info()

        self.assertTrue(display["active"])
        self.assertEqual(display["status"], "ACCEPTANCE")
        self.assertIn("💎", display["label"])
        self.assertEqual(display["exit_code"], 0)

        # Người dùng bấm [100% HOÀN TẤT]
        tw_service.submit_response("ACCEPT")
        resp = teamwork_bridge.check_user_response()
        self.assertIsNotNone(resp)
        self.assertEqual(resp["action"], "ACCEPT")

    def test_04_layout_with_teamwork_chip(self):
        """Test tính toán layout và kích thước khi có chip teamwork."""
        # Active teamwork
        layout_active = horizontal_layout(800, 48, 800, 48, account_name="test@gmail.com", scale_factor=1.0, teamwork_active=True)
        self.assertIn("teamwork", layout_active.boxes)
        tw_box = layout_active.boxes["teamwork"]
        self.assertEqual(tw_box.w, 152.0)

        # Idle teamwork
        layout_idle = horizontal_layout(800, 48, 800, 48, account_name="test@gmail.com", scale_factor=1.0, teamwork_active=False)
        self.assertIn("teamwork", layout_idle.boxes)
        tw_box_idle = layout_idle.boxes["teamwork"]
        self.assertEqual(tw_box_idle.w, 84.0)

    def test_05_native_ide_account_detection(self):
        """Test phát hiện tài khoản native Antigravity IDE từ database state.vscdb."""
        acc = antigravity_service.get_native_antigravity_account()
        # Trên môi trường phát triển này, có Antigravity IDE đang đăng nhập
        self.assertIsNotNone(acc)
        self.assertIn("@", acc["email"])
        self.assertTrue(acc["name"])
        self.assertIn("Antigravity", acc["source"])

    def test_06_fallback_without_cockpit(self):
        """Test cơ chế tự động fallback về Native IDE khi máy không có Cockpit Tool."""
        old_root = antigravity_service.ROOT
        try:
            # Giả lập môi trường máy mới không hề có thư mục .antigravity_cockpit
            antigravity_service.ROOT = Path("C:/nonexistent_cockpit_env_test")
            antigravity_service.ACCOUNTS_FILE = antigravity_service.ROOT / "accounts.json"
            antigravity_service.IDE_ACCOUNTS_FILE = antigravity_service.ROOT / "codex_accounts.json"
            antigravity_service.CURRENT_FILE = antigravity_service.ROOT / "current_account.json"
            antigravity_service.INSTANCES_FILE = antigravity_service.ROOT / "instances.json"
            antigravity_service.IDE_INSTANCES_FILE = antigravity_service.ROOT / "codex_instances.json"
            antigravity_service.ACCOUNT_FILES = antigravity_service.ROOT / "accounts"
            antigravity_service.QUOTA_CACHE = antigravity_service.ROOT / "cache"

            data = antigravity_service.query_antigravity_data()
            self.assertTrue(data.get("healthy"))
            self.assertEqual(data.get("source"), "native-antigravity-ide")
            self.assertNotEqual(data.get("active_email"), "")
            self.assertNotEqual(data.get("active_email"), "Offline")

            # Kiểm tra danh sách tài khoản popup
            accs = antigravity_service.get_cockpit_accounts_with_quota()
            self.assertGreaterEqual(len(accs.get("all", [])), 1)
            active_acc = accs["all"][0]
            self.assertTrue(active_acc.get("is_active"))
            self.assertEqual(active_acc.get("id"), "native_ide")
        finally:
            # Khôi phục trạng thái
            antigravity_service.ROOT = old_root
            antigravity_service.ACCOUNTS_FILE = old_root / "accounts.json"
            antigravity_service.IDE_ACCOUNTS_FILE = old_root / "codex_accounts.json"
            antigravity_service.CURRENT_FILE = old_root / "current_account.json"
            antigravity_service.INSTANCES_FILE = old_root / "instances.json"
            antigravity_service.IDE_INSTANCES_FILE = old_root / "codex_instances.json"
            antigravity_service.ACCOUNT_FILES = old_root / "accounts"
            antigravity_service.QUOTA_CACHE = old_root / "cache" / "quota_api_v1_desktop" / "authorized"


if __name__ == "__main__":
    unittest.main()
