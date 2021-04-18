import os
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

PREFIX = "reporting"


class TestRunSettings(BaseModel):
    display_name: str = "Unnamed"
    build: Optional[str] = None
    environment: Optional[str] = None
    context: Optional[str] = None


class ServerSettings(BaseModel):
    hostname: str
    access_token: str


class NotificationsSettings(BaseModel):
    slack_channels: Optional[str] = None
    ms_teams_channels: Optional[str] = None
    emails: Optional[str] = None


class MilestoneSettings(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


class Settings(BaseModel):
    enabled: bool = True
    project_key: str = "UNKNOWN"
    server: ServerSettings
    run: TestRunSettings = TestRunSettings()
    notifications: NotificationsSettings = NotificationsSettings()
    milestone: MilestoneSettings = MilestoneSettings()


class ZebrunnerSettings:
    def _list_settings(self, model: Type[BaseModel]) -> List:
        setting_names = []
        for field_name, field_value in model.__fields__.items():
            field_list = [field_name]
            if issubclass(field_value.type_, BaseModel):
                inner_fields = self._list_settings(field_value.type_)
                inner_fields = [field_list + inner for inner in inner_fields]
                setting_names += inner_fields
            else:
                setting_names.append(field_list)

        return setting_names

    @staticmethod
    def put_by_path(settings_dict: dict, path: List[str], value: Any) -> None:
        if len(path) == 1:
            settings_dict[path[0]] = value
        else:
            current_dict = settings_dict.get(path[0], {})
            ZebrunnerSettings.put_by_path(current_dict, path[1:], value)
            settings_dict[path[0]] = current_dict

    def load_env(self, path_list: List[List[str]]) -> dict:
        settings: Dict[str, Any] = {}
        for path in path_list:
            env_name = "_".join([PREFIX] + path).upper()
            env_variable = os.getenv(env_name)
            if env_variable is not None:
                ZebrunnerSettings.put_by_path(settings, path, env_variable)

        return settings

    def load_settings(self) -> Settings:
        settings_path_list = self._list_settings(Settings)
        env_settings = self.load_env(settings_path_list)
        settings = Settings(**env_settings)
        return settings

    reporting_enabled: bool = True
    project_key: str
    service_url: str
    access_token: str
    test_run_name: Optional[str]
    build: Optional[str] = None
    env: Optional[str] = None
    context: Optional[str] = None

    # Notifications settings
    emails: Optional[str] = None
    ms_teams_channels: Optional[str] = None
    slack_channels: Optional[str] = None

    send_logs: bool = False

    class Config:
        env_file = ".env"
