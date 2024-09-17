from nonebot.matcher import current_bot, current_event
from nonebot_plugin_userinfo import UserInfo, get_user_info


async def get_operator_info():
    return await get_user_info(
        current_bot.get(),
        (ev := current_event.get()),
        ev.get_user_id(),
    )


def get_display_name_from_info(info: UserInfo) -> str:
    return info.user_displayname or info.user_name
