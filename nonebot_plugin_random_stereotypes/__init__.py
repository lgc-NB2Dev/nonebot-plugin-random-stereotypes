from nonebot.adapters.onebot.v11 import Message
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
# import nonebot
import random

from .data import DATA

catch_str = on_command("发病")


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    random_num = random.randint(1, len(DATA)) - 1

    msg = DATA[random_num].format(target_name=content)

    await catch_str.finish(Message(f'{msg}'), at_sender=True)
