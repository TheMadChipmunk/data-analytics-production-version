"""
Test git workflow for Production Version
- Checks correct git branch and commit history
"""

import pytest
from pathlib import Path
import subprocess

@pytest.fixture
def challenge_dir():
    return Path(__file__).parent.parent

class TestGitWorkflow:
    def test_on_master_branch(self, challenge_dir):
        result = subprocess.run(["git", "branch", "--show-current"], cwd=challenge_dir, capture_output=True, text=True)
        assert result.stdout.strip() == "master", (
            "❌ Not on master branch. Did you create and push to master?"
        )

    def test_has_commits(self, challenge_dir):
        result = subprocess.run(["git", "log", "--oneline"], cwd=challenge_dir, capture_output=True, text=True)
        assert result.stdout.strip(), (
            "❌ No commits found. Did you commit your changes?"
        )
