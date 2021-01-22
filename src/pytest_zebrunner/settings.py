from typing import Optional

from pydantic import BaseSettings


class ZebrunnerSettings(BaseSettings):
    service_url: str
    access_token: str
    zebrunner_project: str
    zebrunner_enabled: bool = True
    suite: Optional[str] = None
    build: Optional[str] = None
    env: Optional[str] = None

    class Config:
        env_file = ".env"
