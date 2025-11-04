from rag.utils.config import get_settings


def test_get_settings_returns_config():
    settings = get_settings()
    assert hasattr(settings, "ES_HOST")
    assert isinstance(settings.ES_HOST, str)
