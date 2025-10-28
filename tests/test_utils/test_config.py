from rag.utils.config import get_settings


def test_get_settings_returns_config():
    settings = get_settings()
    assert hasattr(settings, "ELASTIC_URL")
    assert isinstance(settings.ELASTIC_URL, str)
