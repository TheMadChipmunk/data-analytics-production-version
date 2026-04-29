"""
Test Production Version

Validates that student has:
- Created production environment configuration
- Configured target schema for production
- Set up proper git workflow (main branch)

Tests validate local configuration that supports production setup.
"""

import pytest
from pathlib import Path
import yaml


class TestProductionDeployment:
    """Test production environment configuration."""

    @pytest.fixture
    def greenweez_dbt_dir(self):
        """Get the greenweez_dbt project directory."""
        project_dir = Path(__file__).parent.parent / "greenweez_dbt"
        assert project_dir.exists(), (
            f"❌ greenweez_dbt/ directory not found in {Path(__file__).parent.parent}\n"
            f"   Did you copy your dbt project from the previous challenge? (Section 0)\n"
            f"   First check which challenge directory to copy from: ls ..\n"
            f"   Then run: cp -r ../PREVIOUS-CHALLENGE/greenweez_dbt ."
        )
        return project_dir

    @pytest.fixture
    def dbt_project_file(self, greenweez_dbt_dir):
        """Get dbt_project.yml file."""
        file = greenweez_dbt_dir / "dbt_project.yml"
        assert file.exists(), (
            "❌ dbt_project.yml not found in greenweez_dbt/\n"
            "   Did you create the file and git push it?"
        )
        return file

    @pytest.fixture
    def profiles_file(self, greenweez_dbt_dir):
        """Get profiles.yml file."""
        possible_locations = [
            greenweez_dbt_dir / "profiles.yml",
            Path.home() / ".dbt" / "profiles.yml"
        ]
        for location in possible_locations:
            if location.exists():
                return location
        return None

    def test_dbt_project_has_name(self, dbt_project_file):
        """Project must have a name."""
        with open(dbt_project_file, 'r') as f:
            config = yaml.safe_load(f)
        assert 'name' in config, (
            "❌ dbt_project.yml missing 'name' field\n"
            "   Add project name at the top of dbt_project.yml"
        )
        assert config['name'], (
            "❌ Project name is empty\n"
            "   Set a meaningful project name"
        )

    def test_dbt_project_has_profile(self, dbt_project_file):
        """Project must specify a profile."""
        with open(dbt_project_file, 'r') as f:
            config = yaml.safe_load(f)
        assert 'profile' in config, (
            "❌ dbt_project.yml missing 'profile' field\n"
            "   Add:\n"
            "   profile: your_profile_name\n"
            "   This connects to profiles.yml for environment config"
        )

    def test_profiles_yml_exists(self, profiles_file):
        """profiles.yml should exist for environment configuration."""
        if profiles_file is None:
            pytest.fail(
                "❌ No profiles.yml found\n"
                "   For production deployment, create profiles.yml\n"
                "   with dev and prod targets"
            )

    def test_profiles_has_target_configs(self, profiles_file):
        """profiles.yml should have target configurations."""
        if profiles_file is None:
            pytest.fail("No profiles.yml")

        with open(profiles_file, 'r') as f:
            profiles = yaml.safe_load(f)

        # Get first profile
        if not profiles:
            pytest.fail("profiles.yml is empty")

        profile_name = list(profiles.keys())[0]
        profile = profiles[profile_name]

        assert 'target' in profile, (
            f"❌ Profile '{profile_name}' missing 'target' field\n"
            f"   Specify which target to use by default:\n"
            f"   {profile_name}:\n"
            f"     target: dev"
        )

        assert 'outputs' in profile, (
            f"❌ Profile '{profile_name}' missing 'outputs' field\n"
            f"   Define different targets (dev, prod):\n"
            f"   {profile_name}:\n"
            f"     target: dev\n"
            f"     outputs:\n"
            f"       dev:\n"
            f"         ...\n"
            f"       prod:\n"
            f"         ..."
        )

    def test_has_multiple_targets(self, profiles_file):
        """Should have multiple targets (dev and prod)."""
        if profiles_file is None:
            pytest.fail("No profiles.yml")

        with open(profiles_file, 'r') as f:
            profiles = yaml.safe_load(f)

        profile_name = list(profiles.keys())[0]
        outputs = profiles[profile_name].get('outputs', {})

        target_count = len(outputs)

        if target_count < 2:
            pytest.fail(
                f"❌ Should have at least 2 targets (dev and prod)\n"
                f"   Found: {target_count} target(s)\n"
                f"   Add production target:\n"
                f"   outputs:\n"
                f"     dev:\n"
                f"       type: duckdb\n"
                f"       path: dev.duckdb\n"
                f"     prod:\n"
                f"       type: duckdb\n"
                f"       path: dev_database.duckdb\n"
                f"       schema: analytics_prod"
            )
