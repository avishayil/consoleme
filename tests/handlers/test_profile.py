"""Docstring in public module."""
import os
import sys

import ujson as json
from tornado.testing import AsyncHTTPTestCase

from consoleme.config import config

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(APP_ROOT, ".."))


class TestProfile(AsyncHTTPTestCase):
    def get_app(self):
        from consoleme.routes import make_app

        return make_app(jwt_validator=lambda x: {})

    def test_profile(self):
        headers = {
            config.get("auth.user_header_name"): "user@example.com",
            config.get("auth.groups_header_name"): "groupa,groupb,groupc",
        }

        response = self.fetch("/api/v1/profile", headers=headers)
        self.assertEqual(response.code, 200)
        response_j = json.loads(response.body)
        self.assertEqual(
            response_j,
            {
                "user": "user@example.com",
                "is_contractor": False,
                "employee_photo_url": None,
                "employee_info_url": None,
                "authorization": {
                    "can_edit_policies": False,
                    "can_create_roles": False,
                    "can_delete_roles": False,
                },
                "pages": {
                    "groups": {"enabled": False},
                    "users": {"enabled": False},
                    "policies": {"enabled": True},
                    "self_service": {"enabled": True},
                    "api_health": {"enabled": False},
                    "audit": {"enabled": False},
                    "config": {"enabled": False},
                },
            },
        )