"""
Test schema target for Production Version
- Checks schema target configuration for production
"""

import pytest
from pathlib import Path
import yaml

@pytest.fixture
def greenweez_dbt_dir():
    project_dir = Path(__file__).parent.parent / "greenweez_dbt"
    assert project_dir.exists(), (
        "❌ greenweez_dbt/ directory not found. Did you copy your dbt project?"
    )
    return project_dir

class TestSchemaTarget:
    def test_schema_target_in_profiles(self, greenweez_dbt_dir):
        possible_locations = [
            greenweez_dbt_dir / "profiles.yml",
            Path.home() / ".dbt" / "profiles.yml"
        ]
        profiles_file = next((p for p in possible_locations if p.exists()), None)
        if profiles_file is None:
            pytest.skip("profiles.yml not found")
        with open(profiles_file, 'r') as f:
            content = yaml.safe_load(f)
        if not content:
            pytest.fail("❌ profiles.yml is empty")
        profile_name = list(content.keys())[0]
        outputs = content[profile_name].get('outputs', {})
        prod = outputs.get('prod', {})
        assert 'schema' in prod and prod['schema'], (
            "❌ Production output missing schema config. Add 'schema' to prod target."
        )
