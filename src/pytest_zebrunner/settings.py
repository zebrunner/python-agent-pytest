from typing import Optional

from pydantic import BaseSettings


class ZebrunnerSettings(BaseSettings):
    service_url: str
    access_token: str
    zebrunner_project: str
    reporting_enabled: bool = True
    build: Optional[str] = None
    test_run_name: Optional[str]
    env: Optional[str] = None

    class Config:
        env_file = ".env"
