import random

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .data import DATA

__plugin_meta__ = PluginMetadata(
    name="发病语录",
    description="随机返回一条发病语录",
    usage="命令：发病 [发病对象]\n例如：发病 测试",
)

catch_str = on_command("发病")


@catch_str.handle()
async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
    content = msg.extract_plain_text()

    random_num = random.randint(1, len(DATA)) - 1

    msg = DATA[random_num].format(target_name=content)

    await catch_str.finish(Message(f"{msg}"), at_sender=True)
