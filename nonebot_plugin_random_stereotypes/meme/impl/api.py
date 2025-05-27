from importlib.util import find_spec
from typing import Any, Optional
from typing_extensions import override

from nonebot import require

from ..base import BaseMemeGenerator, MemeMetadata

if not find_spec("nonebot_plugin_memes_api"):
    raise ModuleNotFoundError(
        "No module named 'nonebot_plugin_memes_api'",
        name="nonebot_plugin_memes_api",
    )

require("nonebot_plugin_memes_api")

from nonebot_plugin_memes_api.api import (  # noqa: E402
    Image,
    MemeInfo,
    generate_meme,
    get_meme_info,
)


class MemeGenerator(BaseMemeGenerator):
    @staticmethod
    def transform_meme_info(info: MemeInfo) -> MemeMetadata:
        return MemeMetadata(
            name=info.key,
            min_images=info.params.min_images,
            max_images=info.params.max_images,
            min_texts=info.params.min_texts,
            max_texts=info.params.max_texts,
            has_gender_option=any(
                True for x in info.params.options if x.name == "gender"
            ),
        )

    @override
    async def get_meme(self, name: str) -> MemeMetadata:
        try:
            return self.transform_meme_info(await get_meme_info(name))
        except Exception as e:
            raise ValueError(f"Meme '{name}' not found") from e

    @override
    async def generate(
        self,
        name: str,
        images: Optional[list[tuple[str, bytes]]] = None,
        texts: Optional[list[str]] = None,
        args: Optional[dict[str, Any]] = None,
    ) -> bytes:
        return await generate_meme(
            name,
            [Image(n, d) for n, d in images] if images else [],
            texts or [],
            args or {},
        )


meme_generator = MemeGenerator()
