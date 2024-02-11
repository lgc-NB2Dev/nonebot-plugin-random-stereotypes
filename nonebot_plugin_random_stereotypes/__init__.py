import random

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.plugin import PluginMetadata

from .data import DATA
from .utils import check_CD
from .config import config

__plugin_meta__ = PluginMetadata(
    name="发病语录",
    description="随机返回一条发病语录",
    usage="命令：发病 [发病对象]\n例如：发病 测试",
)

cd = config.stereotypes_cd
aliases = config.stereotypes_aliases
priority = config.stereotypes_priority
block = config.stereotypes_block

catch_str = on_command("发病",
                       aliases=aliases,
                       priority=priority,
                       block=block)


@catch_str.handle(parameterless=[check_CD(cd)])
async def _(matcher: Matcher, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        matcher.set_arg("target", arg)


@catch_str.got("target", "你要对哪个人发病呢？")
async def _(matcher: Matcher, target: Message = Arg("target")):
    target_str = target.extract_plain_text().strip()
    if not target_str:
        await matcher.reject("你发的消息中没有文本，请重新输入！")

    msg = random.choice(DATA).format(target_name=target_str)
    await matcher.finish(message=msg, reply_message=True)
