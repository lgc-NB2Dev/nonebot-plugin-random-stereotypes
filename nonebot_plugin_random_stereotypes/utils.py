from nonebot.matcher import current_bot, current_event
from nonebot_plugin_userinfo import get_user_info


async def get_operator_info():
    return await get_user_info(
        current_bot.get(),
        (ev := current_event.get()),
        ev.get_user_id(),
    )
