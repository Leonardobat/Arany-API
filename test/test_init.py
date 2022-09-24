from arany import create_app
import pytest


class TestInitApp:
    def test_config(self):
        """Test create_app without passing test config."""
        assert not create_app({"DRY_RUN_DB": True}).testing
        assert create_app({"DRY_RUN_DB": True, "TESTING": True}).testing

    def test_db_url_environ(self, monkeypatch):
        """Test DATABASE_URL environment variable."""
        monkeypatch.setenv("DATABASE_URL", "sqlite:///environ")
        app = create_app({"DRY_RUN_DB": True})

        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///environ"
