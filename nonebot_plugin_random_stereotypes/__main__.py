import random
from contextlib import asynccontextmanager, suppress
from datetime import timedelta
from typing import Awaitable, Callable, Dict, Optional

from cookit import format_timedelta
from nonebot import on_command
from nonebot.adapters import Bot as BaseBot, Event as BaseEvent, Message as BaseMessage
from nonebot.exception import RejectedException
from nonebot.matcher import current_bot, current_event, current_matcher
from nonebot.params import CommandArg
from nonebot.permission import SuperUser
from nonebot_plugin_alconna.uniseg import At, Text, UniMessage, UniMsg
from nonebot_plugin_userinfo import UserInfo, get_user_info
from nonebot_plugin_waiter import waiter

from .config import CoolDownKeyType, config
from .cool_down import CoolingDownError, cool_down
from .data import DATA

# region cool down wrapper

cool_down_key_getter_dict: Dict[CoolDownKeyType, Callable[[], Awaitable[str]]] = {}


def cool_down_key_getter(key_type: CoolDownKeyType):
    def deco(func: Callable[[], Awaitable[str]]):
        cool_down_key_getter_dict[key_type] = func
        return func

    return deco


@cool_down_key_getter(CoolDownKeyType.USER)
async def _():
    return current_event.get().get_user_id()


@cool_down_key_getter(CoolDownKeyType.SESSION)
async def _():
    return current_event.get().get_session_id()


superuser_perm = SuperUser()


@asynccontextmanager
async def cool_down_tip_ctx(key: Optional[str] = None):
    bot = current_bot.get()
    ev = current_event.get()

    if await superuser_perm(bot, ev):
        yield
        return

    if not key:
        key = await cool_down_key_getter_dict[config.stereotypes_cd_key_type]()
    try:
        cool_ctx = cool_down.ctx(key)
    except CoolingDownError as e:
        m = current_matcher.get()
        cool_time_str = format_timedelta(timedelta(seconds=e.time_left))
        if e.punished:
            now_cool_time_str = format_timedelta(
                timedelta(seconds=cool_down.cool_down_time),
            )
            await m.finish(
                f"还问？重新计时！"
                f"发电冷却时间已从 {cool_time_str} 重置到 {now_cool_time_str}！",
            )
        if e.queried_count_when_cooling == (cool_down.punish_query_count - 1):
            await m.finish("别在这里发电！")
        await m.finish(f"冷却中，{cool_time_str} 后才可以发电！")

    with cool_ctx:
        yield


# endregion

# region matcher & util func

EXIT_CMDS = {"取消", "退出", "结束", "exit", "e", "quit", "q", "cancel", "c", "0"}


def get_display_name_from_info(info: UserInfo) -> str:
    return info.user_displayname or info.user_name


async def extract_target_str(msg: UniMessage) -> Optional[str]:
    m = current_matcher.get()

    if not msg.has(At):
        return msg.extract_plain_text().strip() or None

    if (at := msg[At, 0]).flag != "user":
        await m.reject("您所 At 的对象不是用户，请重新发送")

    info = await get_user_info(current_bot.get(), current_event.get(), at.target)
    if not info:
        await m.reject("无法获取 At 对象的昵称，请重新发送")

    return get_display_name_from_info(info)


async def prompt_target_name() -> str:
    @waiter(["message"], keep_session=True)
    async def wait_target(msg: UniMsg):
        return msg

    m = current_matcher.get()
    await m.send("请问你要对谁发病呢？可以发送“取消”结束询问")
    while True:
        arg_msg = await wait_target.wait()
        if not arg_msg:
            await m.finish("等待超时，退出询问")
        if arg_msg.extract_plain_text().strip().lower() in EXIT_CMDS:
            await m.finish("已退出询问")
        with suppress(RejectedException):
            target_name = await extract_target_str(arg_msg)
            if target_name:
                return target_name
            await m.finish("无效消息，退出询问")


async def extract_or_prompt_target_name(arg_msg: Optional[UniMessage] = None) -> str:  # noqa: RET503: NoReturn
    if not arg_msg:
        return await prompt_target_name()

    with suppress(RejectedException):
        if target_name := await extract_target_str(arg_msg):
            return target_name

    m = current_matcher.get()
    await m.finish("参数无效")


def create_matcher():
    return on_command(
        "发病",
        aliases=config.stereotypes_aliases,  # type: ignore
        priority=config.stereotypes_priority,
        block=config.stereotypes_block,
    )


cmd_stereotypes = create_matcher()


@cmd_stereotypes.handle()
async def _(
    bot: BaseBot,
    ev: BaseEvent,
    arg_base_msg: BaseMessage = CommandArg(),
):
    async with cool_down_tip_ctx():
        target_name = await extract_or_prompt_target_name(
            await UniMessage.generate(message=arg_base_msg) if arg_base_msg else None,
        )
        msg = UniMessage.text(random.choice(DATA).format(target_name=target_name))
        if config.stereotypes_show_trigger_user_name and (
            trigger_user_info := await get_user_info(bot, ev, ev.get_user_id())
        ):
            trigger_user_name = get_display_name_from_info(trigger_user_info)
            msg.insert(0, Text(f"{trigger_user_name}说：\n----------\n"))
        # do not use finish here otherwise will break cool down
        await msg.send(reply_to=True)


# endregion
