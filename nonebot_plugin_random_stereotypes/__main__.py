import random
from contextlib import asynccontextmanager, suppress
from datetime import timedelta
from typing import Awaitable, Callable, Dict, Optional, Tuple
from typing_extensions import TypeAlias

from cookit import format_timedelta
from nonebot import logger, on_command
from nonebot.adapters import Message as BaseMessage
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
from .meme import get_random_meme_getter
from .utils import get_display_name_from_info, get_operator_info

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

NameInfoOptionalTuple: TypeAlias = Tuple[Optional[str], Optional[UserInfo]]
NameInfoTuple: TypeAlias = Tuple[str, Optional[UserInfo]]


async def extract_target_info(msg: UniMessage) -> Optional[UserInfo]:
    m = current_matcher.get()

    if not msg.has(At):
        return None

    if (at := msg[At, 0]).flag != "user":
        await m.reject("您所 At 的对象不是用户，请重新发送")

    info = await get_user_info(current_bot.get(), current_event.get(), at.target)
    if not info:
        await m.reject("无法获取 At 对象信息，请重新发送")

    return info


async def extract_target_name_info(msg: UniMessage) -> NameInfoOptionalTuple:
    info = await extract_target_info(msg)
    if info:
        return get_display_name_from_info(info), info
    return (msg.extract_plain_text().strip() or None), None


async def prompt_target_name_info(pre_tip: bool = True) -> NameInfoTuple:
    @waiter(["message"], keep_session=True)
    async def wait_target(msg: UniMsg):
        return msg

    m = current_matcher.get()
    if pre_tip:
        await m.send("请问你要对谁发病呢？可以发送“取消”结束询问")
    while True:
        arg_msg = await wait_target.wait()
        if not arg_msg:
            await m.finish("等待超时，退出询问")
        if arg_msg.extract_plain_text().strip().lower() in EXIT_CMDS:
            await m.finish("已退出询问")
        with suppress(RejectedException):
            target_name, info = await extract_target_name_info(arg_msg)
            if target_name:
                return target_name, info
            await m.finish("无效消息，退出询问")


async def extract_or_prompt_target(
    arg_msg: Optional[UniMessage] = None,
) -> NameInfoTuple:  # noqa: RET503: NoReturn
    if not arg_msg:
        return await prompt_target_name_info()

    try:
        target_name, info = await extract_target_name_info(arg_msg)
        if target_name:
            return target_name, info
    except RejectedException:
        return await prompt_target_name_info(pre_tip=False)
    else:
        m = current_matcher.get()
        await m.finish("无效参数")


def create_matcher():
    return on_command(
        "发病",
        aliases=config.stereotypes_aliases,  # type: ignore
        priority=config.stereotypes_priority,
        block=config.stereotypes_block,
    )


cmd_stereotypes = create_matcher()


@cmd_stereotypes.handle()
async def _(arg_base_msg: BaseMessage = CommandArg()):
    async with cool_down_tip_ctx():
        target_name, target_info = await extract_or_prompt_target(
            await UniMessage.generate(message=arg_base_msg) if arg_base_msg else None,
        )

        msg = UniMessage.text(random.choice(DATA).format(target_name=target_name))

        trigger_user_info = None
        if config.stereotypes_show_trigger_user_name and (
            trigger_user_info := await get_operator_info()
        ):
            trigger_user_name = get_display_name_from_info(trigger_user_info)
            msg.insert(0, Text(f"{trigger_user_name}说：\n----------\n"))

        if config.stereotypes_enable_meme and target_info:
            try:
                meme = await get_random_meme_getter().gen_from_ev(
                    target_info,
                    trigger_user_info,
                )
            except Exception:
                logger.exception("Failed to generate meme")
            else:
                msg += UniMessage.image(raw=meme)

        # do not use finish here otherwise will break cool down
        await msg.send(reply_to=True)


# endregion
