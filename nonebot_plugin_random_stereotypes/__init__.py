import random
from nonebot.params import Depends
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.plugin import PluginMetadata

from .data import DATA
from .utils import create_matcher, check_CD
from .config import config

__plugin_meta__ = PluginMetadata(
    name="发病语录",
    description="随机返回一条发病语录",
    usage="命令：发病 [发病对象]\n例如：发病 测试",
)

catch_str = create_matcher()


@catch_str.handle(parameterless=[Depends(check_CD)])
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
