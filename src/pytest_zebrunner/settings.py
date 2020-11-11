from typing import Optional

from pydantic import BaseSettings


class ZebrunnerSettings(BaseSettings):
    service_url: str
    access_token: str
    zebrunner_project: str
    zebrunner_enabled: bool = True
    driver_instance_name: Optional[str] = None
    suite: Optional[str] = None
    build: Optional[str] = None
    env: Optional[str] = None

    class Config:
        env_file = ".env"
