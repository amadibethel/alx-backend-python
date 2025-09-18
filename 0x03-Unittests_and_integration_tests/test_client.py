#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, mock_get_json, org_name):
        """Test that GithubOrgClient.org returns the expected value."""
        test_payload = {"key": "value"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()
