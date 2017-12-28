"""
Test configuration
See more about fixtures at
https://docs.pytest.org/en/latest/fixture.html
"""
try: import simplejson as json 
except ImportError: import json
import pytest
from gnucash_portfolio.lib.settings import Settings
from gnucash_portfolio.bookaggregate import BookAggregate

# pylint: disable=redefined-outer-name


''' Fixture for the Settings, to use in-memory database.
Use global scope in order to use the same instance.
Scopes: class, module, session.
Class is the default, and does not need to be specified. '''
@pytest.fixture(scope="session")
def settings() -> Settings:
    """ GnuCash Portfolio Settings for tests """
    config_json = json.loads('{ "gnucash.database": ":memory:" }')

    config = Settings(config_json)

    assert config.database_path == ":memory:"

    return config

@pytest.fixture(scope="session")
def settings_db() -> Settings:
    """ Settings for the real db file """
    config_json = json.loads('{ "gnucash.database": "../data/test.gnucash" }')
    config = Settings(config_json)
    return config


@pytest.fixture(scope="module")
def svc(settings) -> BookAggregate:
    """ Module-level book aggregate, using test settings """
    return BookAggregate(settings)

@pytest.fixture(scope="module")
def svc_db(settings_db) -> BookAggregate:
    """ Book aggregate that uses the real database file (test.gnucash) """
    return BookAggregate(settings_db)


class TestSettings(object):
    """
    Declares the settings and Book Aggregate as autouse.
    This means that individual tests do not need to mark the fixture explicitly.
    It is more useful when there is functionality that needs to be executed than for dependency
    injection.
    """
    @pytest.fixture(autouse=True, scope="session")
    def settings(self):
        """ Returns the test settings json """
        return settings()
        # yield
        # teardown

    @pytest.fixture(autouse=True, scope="session")
    def svc(self):
        """ global Book Aggregate for all tests """
        return svc(self.settings)
