from typing import Any, Optional
from typing_extensions import override

from meme_generator import Image, Meme, get_meme
from nonebot import get_available_plugin_names, get_driver

from ..base import BaseMemeGenerator, MemeMetadata


class MemeGenerator(BaseMemeGenerator):
    @staticmethod
    def transform_meme(meme: Meme):
        return MemeMetadata(
            name=meme.key,
            min_images=meme.info.params.min_images,
            max_images=meme.info.params.max_images,
            min_texts=meme.info.params.min_texts,
            max_texts=meme.info.params.max_texts,
            has_gender_option=any(
                True for x in meme.info.params.options if x.name == "gender"
            ),
        )

    @override
    async def get_meme(self, name: str) -> MemeMetadata:
        return self.transform_meme(get_meme(name))

    @override
    async def generate(
        self,
        name: str,
        images: Optional[list[tuple[str, bytes]]] = None,
        texts: Optional[list[str]] = None,
        args: Optional[dict[str, Any]] = None,
    ) -> bytes:
        r = get_meme(name).generate(
            images=[Image(n, d) for n, d in images] if images else [],
            texts=texts or [],
            options=args or {},
        )
        if isinstance(r, bytes):
            return r
        raise RuntimeError(f"{type(r).__name__}: {r}")


if "nonebot_plugin_memes" not in get_available_plugin_names():
    from meme_generator.resources import check_resources_in_background

    driver = get_driver()

    @driver.on_startup
    async def _():
        check_resources_in_background()


meme_generator = MemeGenerator()
