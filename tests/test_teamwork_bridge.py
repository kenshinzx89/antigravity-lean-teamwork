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
WIDGET_ROOT = Path(r"c:\Users\tient\Desktop\Du An\AntigravityWidget")

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(WIDGET_ROOT))

import teamwork_bridge
from core.teamwork_service import get_teamwork_service
from core.layout import horizontal_layout, calculate_account_chip_width


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


if __name__ == "__main__":
    unittest.main()
