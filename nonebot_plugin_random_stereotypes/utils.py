from typing import Union

from nonebot_plugin_uninfo import Member, User


def get_display_name_from_info(info: Union["Member", "User"]) -> str:
    if isinstance(info, Member):
        if info.nick:
            return info.nick
        info = info.user
    return info.nick or info.name or info.id
