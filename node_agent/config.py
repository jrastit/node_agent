from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["./settings/settings.yaml", "./settings/.secrets.yaml"],
    environments=True,
)


def get_databaste_uri():
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
