"""Commonly used sets of settings."""

from configurator.fields import String, Integer, Url
from configurator.main import BaseSettings


class OracleConnectorSettings(BaseSettings):
    """Setting required for connection to oracle database."""
    host = Url()
    port = Integer()
    user = String()
    password = String()
    sid = String()

    def get_connection_url(self):
        """Get connection url for sql alchemy"""
        return f"oracle://{self.user}:{self.password}@{self.host}:{self.port}/{self.sid}"


class BoxSettings(BaseSettings):
    """Settings required for connection to box.com"""

    class BoxAppSettings(BaseSettings):
        """Application settings for box.com"""

        class BoxAuthorization(BaseSettings):
            """Authorization for box.com"""
            publicKeyID = String()
            privateKey = String()
            passphrase = String()

        clientID = String()
        clientSecret = String()
        appAuth = BoxAuthorization()

    boxAppSettings = BoxAppSettings()
    enterpriseID = String()
