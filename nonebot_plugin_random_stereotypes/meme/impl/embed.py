import asyncio
from typing import Any, Dict, List, Optional
from typing_extensions import override

from meme_generator import Meme, get_meme
from nonebot import get_available_plugin_names, get_driver
from nonebot.utils import run_sync

from ..base import BaseMemeGenerator, MemeMetadata


class MemeGenerator(BaseMemeGenerator):
    @staticmethod
    def transform_meme(meme: Meme):
        return MemeMetadata(
            name=meme.key,
            min_images=meme.params_type.min_images,
            max_images=meme.params_type.max_images,
            min_texts=meme.params_type.min_texts,
            max_texts=meme.params_type.max_texts,
        )

    @override
    async def get_meme(self, name: str) -> MemeMetadata:
        return self.transform_meme(get_meme(name))

    @override
    async def generate(
        self,
        name: str,
        images: Optional[List[bytes]] = None,
        texts: Optional[List[str]] = None,
        args: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        return (
            await run_sync(get_meme(name))(
                images=images or [],
                texts=texts or [],
                args=args or {},
            )
        ).getvalue()


if "nonebot_plugin_memes" not in get_available_plugin_names():
    from meme_generator.download import check_resources

    driver = get_driver()

    @driver.on_startup
    async def _():
        asyncio.create_task(check_resources())


meme_generator = MemeGenerator()
