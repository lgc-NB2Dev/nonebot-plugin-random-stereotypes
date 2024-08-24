import random
from nonebot.params import Depends
from nonebot.adapters.onebot.v11 import Bot,Message, MessageEvent , MessageSegment, Message, GroupMessageEvent
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
async def _(matcher: Matcher,bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = event.get_message()
    if "at" in msg:
        gid = event.group_id  # 获取群号
        uid = event.user_id
        qid = await get_at(event)
        target_str = ""
        print(qid)
        if not qid:
                if arg.extract_plain_text().strip():
                    matcher.set_arg("target", arg)
        else:
            await bot.call_api('get_group_member_list', group_id=gid)
            member_info = await bot.get_group_member_info(group_id=gid, user_id=qid)
            card_name = member_info['card'] if member_info['card'] else member_info['nickname']
            target_str = card_name
            print(qid)
            await bot.call_api('get_group_member_list', group_id=gid)
            member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
            card_name = member_info['card'] if member_info['card'] else member_info['nickname']
            msg1 = f"{card_name}说：\n-----------\n"
            msg = msg1 + random.choice(DATA).format(target_name=target_str)
            await matcher.finish(message=msg, reply_message=True)
    else:
        if arg.extract_plain_text().strip():
            matcher.set_arg("target", arg)

@catch_str.got("target", "你要对哪个人发病呢？")
async def _(matcher: Matcher,bot: Bot, event: GroupMessageEvent, target: Message = Arg("target")):
    target_str = target.extract_plain_text().strip()
    gid = event.group_id  # 获取群号
    uid = event.user_id
    qid = await get_at(event)
    print(qid)
    if not target_str:
        await bot.call_api('get_group_member_list', group_id=gid)
        member_info = await bot.get_group_member_info(group_id=gid, user_id=qid)
        card_name = member_info['card'] if member_info['card'] else member_info['nickname']
        target_str = card_name
        print(target_str)
        if not card_name:
            await matcher.reject("你发的消息中没有文本，请重新输入！")

    msg = random.choice(DATA).format(target_name=target_str)
    await matcher.finish(message=msg, reply_message=True)

async def get_at(event: GroupMessageEvent) -> int:
    """获取被艾特用户 ID"""
    msg = event.get_message()
    for msg_seg in msg:
        if msg_seg.type == "at":
            return -1 if msg_seg.data["qq"] == "all" else int(msg_seg.data["qq"])
    return -1
