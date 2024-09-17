from importlib.util import find_spec
from typing import Any, Dict, List, Optional
from typing_extensions import override

from nonebot import require

from ..base import BaseMemeGenerator, MemeMetadata

if not find_spec("nonebot_plugin_memes_api"):
    raise ModuleNotFoundError(
        "No module named 'nonebot_plugin_memes_api'",
        name="nonebot_plugin_memes_api",
    )

require("nonebot_plugin_memes_api")

from nonebot_plugin_memes_api.request import (  # noqa: E402
    MemeInfo,
    generate_meme,
    get_meme_info,
)


class MemeGenerator(BaseMemeGenerator):
    @staticmethod
    def transform_meme_info(info: MemeInfo) -> MemeMetadata:
        return MemeMetadata(
            name=info.key,
            min_images=info.params_type.min_images,
            max_images=info.params_type.max_images,
            min_texts=info.params_type.min_texts,
            max_texts=info.params_type.max_texts,
        )

    @override
    async def get_meme(self, name: str) -> MemeMetadata:
        return self.transform_meme_info(await get_meme_info(name))

    @override
    async def generate(
        self,
        name: str,
        images: Optional[List[bytes]] = None,
        texts: Optional[List[str]] = None,
        args: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        return await generate_meme(name, images or [], texts or [], args or {})


meme_generator = MemeGenerator()
