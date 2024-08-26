from enum import Enum, auto
from typing import Set

from nonebot import get_plugin_config
from pydantic import BaseModel


class CoolDownKeyType(str, Enum):
    USER = auto()
    SESSION = auto()


class ConfigModel(BaseModel):
    superusers: Set[str]

    stereotypes_cd: int = 1800
    stereotypes_count: int = 3
    stereotypes_count_time: int = 1800
    stereotypes_punish_count: int = 5
    stereotypes_cd_key_type: CoolDownKeyType = CoolDownKeyType.USER

    stereotypes_show_trigger_user_name: bool = True

    stereotypes_aliases: Set[str] = {"发电", "发癫"}
    stereotypes_priority: int = 100
    stereotypes_block: bool = False


config = get_plugin_config(ConfigModel)
