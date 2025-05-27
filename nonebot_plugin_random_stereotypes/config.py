from enum import auto
from pathlib import Path
from typing import Any, Union

from cookit import StrEnum
from cookit.pyd import field_validator, type_validate_python
from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class CoolDownKeyType(StrEnum):
    USER = auto()
    SESSION = auto()


class MemeSource(StrEnum):
    AUTO = auto()
    EMBED = auto()
    API = auto()


class MemeConfig(BaseModel):
    name: str
    target_first: bool = False
    additional_images: list[Path] = Field(default_factory=list)
    additional_texts: list[str] = Field(default_factory=list)
    additional_args: dict[str, Any] = Field(default_factory=dict)


class ConfigModel(BaseModel):
    superusers: set[str]

    stereotypes_cd: int = 1800
    stereotypes_count: int = 3
    stereotypes_count_time: int = 1800
    stereotypes_punish_count: int = 5
    stereotypes_cd_key_type: CoolDownKeyType = CoolDownKeyType.USER

    stereotypes_show_trigger_user_name: bool = True

    stereotypes_enable_meme: bool = True
    stereotypes_meme_source: MemeSource = MemeSource.AUTO
    stereotypes_memes: list[MemeConfig] = Field(
        default_factory=lambda: [
            MemeConfig(name="kiss"),
            MemeConfig(name="suck"),
            MemeConfig(name="rub"),
            MemeConfig(name="little_angel"),
        ],
    )

    stereotypes_aliases: set[str] = {"发电", "发癫"}
    stereotypes_priority: int = 100
    stereotypes_block: bool = False

    @field_validator("stereotypes_memes", mode="before")
    def _(cls, v: Any):  # noqa: N805
        validated = type_validate_python(list[Union[MemeConfig, str]], v)
        return [MemeConfig(name=i) if isinstance(i, str) else i for i in validated]


config = get_plugin_config(ConfigModel)
