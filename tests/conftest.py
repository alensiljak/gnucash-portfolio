"""
Test configuration
See more about fixtures at
https://docs.pytest.org/en/latest/fixture.html
"""
import json
import pytest
from gnucash_portfolio.lib.settings import Settings

# Fixture for the Settings, to use in-memory database.
# Use global scope in order to use the same instance.
@pytest.fixture(scope="module")
def settings() -> Settings:
    """ GnuCash Portfolio Settings for tests """
    config_json = json.loads('{ "gnucash.database": ":memory:" }')

    config = Settings(config_json)

    assert config.database_path == ":memory:"

    return config
