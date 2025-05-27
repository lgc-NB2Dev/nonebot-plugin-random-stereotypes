from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class MemeMetadata:
    name: str
    min_images: int
    max_images: int
    min_texts: int
    max_texts: int
    has_gender_option: bool


class BaseMemeGenerator(ABC):
    @abstractmethod
    async def get_meme(self, name: str) -> MemeMetadata: ...

    @abstractmethod
    async def generate(
        self,
        name: str,
        images: Optional[list[tuple[str, bytes]]] = None,
        texts: Optional[list[str]] = None,
        args: Optional[dict[str, Any]] = None,
    ) -> bytes: ...
