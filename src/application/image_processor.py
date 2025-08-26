from domain.schemas import BaseImage, ImageProcessor
from rembg import remove
from PIL import Image


class ImageProcessorAdapter(ImageProcessor):
    def process(self, image: BaseImage) -> BaseImage:
        result = remove(image["data"])
        if isinstance(result, Image.Image):
            result = result.tobytes()
        return {
            "mimetype": image["mimetype"],
            "data": bytearray(result),
            "ext": image["ext"],
        }
