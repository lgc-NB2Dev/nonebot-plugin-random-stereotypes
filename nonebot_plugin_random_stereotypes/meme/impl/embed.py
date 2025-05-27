from typing import Any, Optional, Union
from typing_extensions import override

from meme_generator import (
    DeserializeError,
    Image,
    ImageAssetMissing,
    ImageDecodeError,
    ImageEncodeError,
    ImageNumberMismatch,
    Meme,
    MemeFeedback,
    TextNumberMismatch,
    TextOverLength,
    get_meme,
)

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

    @staticmethod
    def format_error(
        e: Union[
            ImageDecodeError,
            ImageEncodeError,
            ImageAssetMissing,
            DeserializeError,
            ImageNumberMismatch,
            TextNumberMismatch,
            TextOverLength,
            MemeFeedback,
        ],
    ) -> str:
        if isinstance(e, ImageDecodeError):
            return f"Image decode error: {e.error}"
        if isinstance(e, ImageEncodeError):
            return f"Image encode error: {e.error}"
        if isinstance(e, ImageAssetMissing):
            return f"Image asset missing: {e.path}"
        if isinstance(e, DeserializeError):
            return f"Deserialize error: {e.error}"
        if isinstance(e, ImageNumberMismatch):
            return (
                f"Image number mismatch: expected between {e.min} and {e.max}, "
                f"got {e.actual}"
            )
        if isinstance(e, TextNumberMismatch):
            return (
                f"Text number mismatch: expected between {e.min} and {e.max}, "
                f"got {e.actual}"
            )
        if isinstance(e, TextOverLength):
            return f"Text over length: '{e.text}'"
        if isinstance(e, MemeFeedback):
            return f"Meme feedback: {e.feedback}"
        return str(e)

    @override
    async def get_meme(self, name: str) -> MemeMetadata:
        meme = get_meme(name)
        if not meme:
            raise ValueError(f"Meme '{name}' not found")
        return self.transform_meme(meme)

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
        raise RuntimeError(self.format_error(r))


meme_generator = MemeGenerator()
