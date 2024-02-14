from typing import Set

import nonebot
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    stereotypes_cd: int = 1800
    stereotypes_aliases: Set = set({"发电", "发癫"})
    stereotypes_count: int = 3
    stereotypes_priority: int = 100
    stereotypes_block: bool = False


global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config)
superusers = global_config.superusers
