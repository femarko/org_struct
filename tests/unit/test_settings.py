from src.org_struct.config import (
    Settings,
    get_settings,
)



def test_db_url() -> None:
    settings = Settings(
        postgres_host="localhost",
        db_port=5432,
        postgres_user="user",
        postgres_password="pass",
        postgres_db="app"
    )
    assert settings.db_url == (
        "postgresql://user:pass@localhost:5432/app"
    )


def test_get_settings_cached():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
