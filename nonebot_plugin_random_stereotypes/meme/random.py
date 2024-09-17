import asyncio
import random
from dataclasses import dataclass
from typing import Iterable, List, Optional, cast

from nonebot import logger
from nonebot_plugin_userinfo import ImageSource, UserInfo

from ..config import MemeConfig
from ..utils import get_display_name_from_info, get_operator_info
from .base import BaseMemeGenerator, MemeArgUserInfo, MemeMetadata


def calc_need_num(
    expected_min: int,
    expected_max: int,
    additional_len: int,
    actual_need_min: int,
    actual_need_max: int,
) -> Optional[int]:
    """
    计算符合期望区间内的最大所需数
    返回 None 表示不符合要求
    返回值应在 expected_min 和 expected_max 之间

    Args:
        expected_min: 期望区间最小值
        expected_max: 期望区间最大值
        additional_len: 附加数量
        actual_need_min: 算上附加数量的需求区间最小值
        actual_need_max: 算上附加数量的需求区间最大值
    """

    # 计算实际需求范围的边界
    adjusted_min = actual_need_min - additional_len
    adjusted_max = actual_need_max - additional_len

    # 计算符合要求的最大需求值
    result_min = max(expected_min, adjusted_min)
    result_max = min(expected_max, adjusted_max)

    # 确定返回值
    if result_min <= result_max:
        return result_max
    return None


@dataclass
class RandomMemeGenData:
    config: MemeConfig
    meme: MemeMetadata
    expected_image_num: int


class RandomMemeGetter:
    def __init__(
        self,
        generator: BaseMemeGenerator,
        min_images_expected: int,
        max_images_expected: int,
    ) -> None:
        self.generator: BaseMemeGenerator = generator
        self.min_images_expected: int = min_images_expected
        self.max_images_expected: int = max_images_expected
        self.data: List[RandomMemeGenData] = []

    def get_gen_data(self, config: MemeConfig, meme: MemeMetadata) -> RandomMemeGenData:
        def calc_ensure(
            type_name: str,
            expected_min: int,
            expected_max: int,
            additional_len: int,
            actual_need_min: int,
            actual_need_max: int,
        ) -> int:
            v = calc_need_num(
                expected_min,
                expected_max,
                additional_len,
                actual_need_min,
                actual_need_max,
            )
            if v is None:
                raise ValueError(
                    f"Cannot use meme {meme.name}, "
                    f"because the required number of {type_name} is not compatible. "
                    f"Meme needed {actual_need_min} ~ {actual_need_max}, "
                    f"should satisfy "
                    f"{expected_min + additional_len} ~ "
                    f"{expected_max + additional_len}.",
                )
            return v

        expected_image_num = calc_ensure(
            "images",
            self.min_images_expected,
            self.max_images_expected,
            len(config.additional_images),
            meme.min_images,
            meme.max_images,
        )
        calc_ensure(
            "texts",
            0,
            0,
            len(config.additional_texts),
            meme.min_texts,
            meme.max_texts,
        )
        return RandomMemeGenData(
            config=config,
            meme=meme,
            expected_image_num=expected_image_num,
        )

    async def append(self, config: MemeConfig):
        m = await self.generator.get_meme(config.name)
        try:
            data = self.get_gen_data(config, m)
        except ValueError as e:
            logger.warning(f"Skip using meme {config.name}: {e}")
        else:
            self.data.append(data)

    async def extend(self, configs: Iterable[MemeConfig]):
        await asyncio.gather(*(self.append(name) for name in configs))

    def get(self) -> RandomMemeGenData:
        if not self.data:
            raise ValueError("No meme available")
        return random.choice(self.data)

    async def gen_from_ev(
        self,
        target_info: UserInfo,
        operator_info: Optional[UserInfo] = None,
    ) -> bytes:
        data = self.get()

        if not target_info.user_avatar:
            raise ValueError("No target user avatar data")

        user_infos = [target_info]
        if data.expected_image_num > 1:
            if not operator_info:
                operator_info = await get_operator_info()
            if (not operator_info) or (not operator_info.user_avatar):
                raise ValueError("No operation user avatar data")

            if data.config.target_first:
                user_infos.append(operator_info)
            else:
                user_infos.insert(0, operator_info)

        user_images = await asyncio.gather(
            *(cast(ImageSource, x.user_avatar).get_image() for x in user_infos),
        )

        return await self.generator.generate(
            data.config.name,
            [
                *(user_images or []),
                *(x.read_bytes() for x in data.config.additional_images),
            ],
            data.config.additional_texts,
            {
                "user_infos": [
                    MemeArgUserInfo(
                        name=get_display_name_from_info(x),
                        gender=x.user_gender,  # type: ignore
                    )
                    for x in user_infos
                ],
                **data.config.additional_args,
            },
        )
