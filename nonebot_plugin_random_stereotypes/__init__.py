# ruff: noqa: E402

from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_waiter")
require("nonebot_plugin_alconna")
require("nonebot_plugin_userinfo")

from . import __main__ as __main__
from .config import ConfigModel

__version__ = "0.4.0"
__plugin_meta__ = PluginMetadata(
    name="发病语录",
    description="随机返回一条发病语录",
    usage="命令：发病 [发病对象]\n例如：发病 测试",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-random-stereotypes",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_waiter",
        "nonebot_plugin_alconna",
        "nonebot_plugin_userinfo",
    ),
    extra={},
)
