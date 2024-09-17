from typing import Callable, Dict, Optional

from nonebot import get_driver, logger

from ..config import MemeSource, config
from .base import (
    BaseMemeGenerator as BaseMemeGenerator,
    MemeArgUserInfo as MemeArgUserInfo,
    MemeMetadata as MemeMetadata,
)
from .random import RandomMemeGetter as RandomMemeGetter

_meme_generator: Optional[BaseMemeGenerator] = None
_random_meme_getter: Optional[RandomMemeGetter] = None


generator_source_func_map: Dict[MemeSource, Callable[[], BaseMemeGenerator]] = {}


def generator_source(source: MemeSource):
    def deco(func: Callable[[], BaseMemeGenerator]):
        generator_source_func_map[source] = func
        return func

    return deco


@generator_source(MemeSource.EMBED)
def import_embed_source() -> BaseMemeGenerator:
    try:
        from .impl.embed import meme_generator
    except ImportError as e:
        raise ImportError(
            "Import embed meme source failed,"
            " consider running `pip install nonebot-plugin-random-stereotypes[meme]`"
            " to install required deps",
        ) from e
    return meme_generator


@generator_source(MemeSource.API)
def import_api_source() -> BaseMemeGenerator:
    try:
        from .impl.api import meme_generator
    except ImportError as e:
        raise ImportError(
            "Import api meme source failed,"
            " consider running `pip install nonebot-plugin-random-stereotypes[meme-api]`"
            " to install required deps",
        ) from e
    return meme_generator


def import_meme_generator() -> BaseMemeGenerator:
    if config.stereotypes_meme_source is not MemeSource.AUTO:
        v = generator_source_func_map[config.stereotypes_meme_source]()
        logger.info(f"Using {config.stereotypes_meme_source.value} meme source")
        return v

    for source, func in generator_source_func_map.items():
        try:
            v = func()
        except ImportError as e:
            logger.opt(exception=e).debug("Import source failed")
        else:
            logger.info(f"Using {source.value} meme source")
            return v

    raise ImportError(
        "Cannot find usable meme source,"
        " consider running `pip install nonebot-plugin-random-stereotypes[meme]`"
        " to use embed source",
    )


def get_meme_generator() -> BaseMemeGenerator:
    global _meme_generator
    if _meme_generator is not None:
        return _meme_generator
    v = import_meme_generator()
    _meme_generator = v
    return v


async def init_random_meme_getter():
    global _random_meme_getter
    _random_meme_getter = RandomMemeGetter(
        get_meme_generator(),
        min_images_expected=1,
        max_images_expected=2,
    )

    try:
        await _random_meme_getter.extend(config.stereotypes_memes)
    except Exception:
        logger.exception("Failed to load memes, will disable meme feature")
        config.stereotypes_enable_meme = False
        return

    if not _random_meme_getter.data:
        logger.warning("No meme available, will disable meme feature")
        config.stereotypes_enable_meme = False


def get_random_meme_getter() -> RandomMemeGetter:
    if not _random_meme_getter:
        raise ValueError("Random meme getter not initialized")
    return _random_meme_getter


if config.stereotypes_enable_meme:
    try:
        get_meme_generator()
    except Exception as e:
        logger.warning("Cannot construct meme generator, will disable meme feature")
        logger.warning(str(e))
        logger.opt(exception=e).debug("Stacktrace")
        config.stereotypes_enable_meme = False

if config.stereotypes_enable_meme:
    driver = get_driver()
    driver.on_startup(init_random_meme_getter)
