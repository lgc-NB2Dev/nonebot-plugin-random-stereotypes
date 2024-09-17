from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MemeMetadata:
    name: str
    min_images: int
    max_images: int
    min_texts: int
    max_texts: int


class BaseMemeGenerator(ABC):
    @abstractmethod
    async def get_meme(self, name: str) -> MemeMetadata: ...

    @abstractmethod
    async def generate(
        self,
        name: str,
        images: Optional[List[bytes]] = None,
        texts: Optional[List[str]] = None,
        args: Optional[Dict[str, Any]] = None,
    ) -> bytes: ...
