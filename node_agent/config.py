from pathlib import Path
from dynaconf import Dynaconf

ROOT_PATH = Path(__file__).resolve().parents[1]
SETTINGS_YAML = ROOT_PATH / "settings" / "settings.yaml"
SECRETS_YAML  = ROOT_PATH / "settings" / ".secrets.yaml"

print (f"Loading settings from {SETTINGS_YAML} and {SECRETS_YAML}")

settings = Dynaconf(
    root_path=str(ROOT_PATH),
    envvar_prefix="DYNACONF",
    settings_files=[str(SETTINGS_YAML), str(SECRETS_YAML)],
    environments=True,
)


def get_database_uri():
    db_user = settings.get("db_user")
    db_password = settings.get("db_password")
    db_host = settings.get("db_host")
    db_port = settings.get("db_port")
    db_name = settings.get("db_name")

    if db_port:
        return (
            f"postgresql+psycopg2://{db_user}:"
            + f"{db_password}@{db_host}:{db_port}/{db_name}"
        )
    return (
        f"postgresql+psycopg2://{db_user}:"
        + f"{db_password}@{db_host}/{db_name}"
    )
