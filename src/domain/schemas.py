from typing import TypedDict, Union
import io
from abc import ABC, abstractmethod


class BaseImage(TypedDict):
    mimetype: str
    ext: str
    data: bytearray


class InvalidImage(Exception):
    pass


class ImageProcessingError(Exception):
    pass


class ImageParser(ABC):
    @abstractmethod
    def parse(self, raw_data: Union[io.IOBase, str]) -> BaseImage:
        pass


class ImageProcessor(ABC):
    @abstractmethod
    def process(self, image: BaseImage) -> BaseImage:
        pass
