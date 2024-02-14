from collections import defaultdict
from typing import AsyncGenerator

from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot import on_command
from .config import superusers, config

cd_dict = defaultdict(lambda: [0, 0])
cd = config.stereotypes_cd
aliases = config.stereotypes_aliases
count = config.stereotypes_count
priority = config.stereotypes_priority
block = config.stereotypes_block


def create_matcher():
    return on_command("发病", aliases=aliases, priority=priority, block=block)


async def check_CD(
        matcher: Matcher, event: MessageEvent
) -> AsyncGenerator[None, None]:
    user_id = event.get_user_id()
    last_time, cd_count = cd_dict[user_id]
    last_time += cd
    cd_dict[user_id][1] += 1
    if event.time < last_time:
        if cd_count == count + 1:
            msg = "别在这里发电!"
        elif cd_count > count + 1:
            cd_dict[user_id][0] = event.time
            msg = f"还问?重新计时!现在{last_time - event.time} 秒后才可以发电!"
        else:
            msg = f"冷却中,{last_time - event.time} 秒后才可以发电!"
        await matcher.finish(msg, at_sender=True)
    yield
    if str(user_id) not in superusers:
        if cd_dict[user_id][1] == count:  # 启动计时器
            cd_dict[user_id][0] = event.time
        elif cd_dict[user_id][1] > count:  # 重置计时器、计数器
            cd_dict[user_id] = [0, 0]
