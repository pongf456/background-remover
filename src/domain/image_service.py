from typing import Union
from .schemas import ImageParser, ImageProcessor, InvalidImage
import io


class ImageService:
    def __init__(self, parser: ImageParser, processor: ImageProcessor):
        self.__parser = parser
        self.__processor = processor

    def remove_background(self, raw_data: Union[io.IOBase, str]):
        raw_image = self.__parser.parse(raw_data)
        if not "image" in raw_image["mimetype"]:
            raise InvalidImage()
        processed_image = self.__processor.process(raw_image)
        return processed_image
