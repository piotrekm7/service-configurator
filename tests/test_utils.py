"""Test utility settings classes"""
from unittest import TestCase
from configurator.utils import OracleConnectorSettings


class TestOracleSettings(TestCase):
    """Test OracleSettings"""

    def test_get_connection_url(self):
        """Test connection url"""
        oracle_settings = OracleConnectorSettings()
        oracle_settings.from_dict({
            "host": "http://localhost",
            "port": 1521,
            "user": "user",
            "password": "password",
            "sid": "sid"
        })
        self.assertEqual('oracle://user:password@http://localhost:1521/sid', oracle_settings.get_connection_url())
