from collections import defaultdict
from typing import AsyncGenerator, Any

from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import Depends
from nonebot.matcher import Matcher

from .config import superusers

cd_dict = defaultdict(lambda: [0, 0])


def check_CD(cd_time: int) -> Any:
    async def cooldown(
            matcher: Matcher, event: MessageEvent
    ) -> AsyncGenerator[None, None]:
        user_id = event.get_user_id()
        last_time, cd_count = cd_dict[user_id]
        last_time += cd_time
        cd_dict[user_id][1] += 1

        if str(user_id) not in superusers and event.time < last_time:
            if cd_count > 1:
                msg = "别在这里发电!"
            else:
                msg = f"冷却中,{last_time - event.time} 秒后才可以发电!"
            await matcher.finish(msg, at_sender=True)

        yield
        cd_dict[user_id] = [event.time, 0]

    return Depends(cooldown)
