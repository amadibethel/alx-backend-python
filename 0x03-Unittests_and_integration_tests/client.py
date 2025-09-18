#!/usr/bin/env python3
"""
GithubOrgClient module to access GitHub organization information.
"""

from typing import List, Dict, Optional
from utils import get_json


class GithubOrgClient:
    """
    Client to interact with the GitHub API for a given organization.
    """

    def __init__(self, org_name: str):
        """
        Initialize the client with the organization name.

        Args:
            org_name (str): The GitHub organization name.
        """
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """
        Retrieve the organization information from GitHub API.

        Returns:
            dict: Organization JSON data.
        """
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """
        Get the URL of public repositories.

        Returns:
            str: URL of public repositories.
        """
        return self.org.get("repos_url", "")

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """
        List the names of public repositories.

        Args:
            license (str, optional): Filter by license key. Defaults to None.

        Returns:
            list: List of repository names.
        """
        repos_data = get_json(self._public_repos_url)
        repo_names = [
            repo["name"] for repo in repos_data
            if license is None or self.has_license(repo, license)
        ]
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """
        Check if a repository has a specific license.

        Args:
            repo (dict): Repository data.
            license_key (str): License key to check.

        Returns:
            bool: True if license matches, False otherwise.
        """
        repo_license = repo.get("license")
        if repo_license is None:
            return False
        return repo_license.get("key") == license_key
