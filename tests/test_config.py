""" Tests for the config reader """

from gnucash_portfolio.lib.settings import Settings


def test_creation():
    """ See if the config file gets created """
    settings = Settings()
    
    assert settings
    assert settings.settings_file_exists()
