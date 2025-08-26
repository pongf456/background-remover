from domain.schemas import ImageParser, BaseImage, InvalidImage, ImageProcessingError
from typing import Union
import mimetypes
import io
import filetype


class ImageParserAdapter(ImageParser):
    def __to_stream(self, data: Union[io.IOBase, str]) -> io.IOBase:
        if isinstance(data, str):
            try:
                file = open(data, "rb")
                return file
            except FileNotFoundError:
                raise InvalidImage()
        else:
            return data

    def parse(self, raw_data: Union[io.IOBase, str]) -> BaseImage:
        raw_data = self.__to_stream(raw_data)
        try:
            raw_data.seek(0)
            data = raw_data.read()
            mimetype = filetype.guess_mime(data)
            if not mimetype:
                raise InvalidImage()
            ext = mimetypes.guess_extension(mimetype)
            if not ext:
                raise InvalidImage()
            raw_data.close()
            return BaseImage({"mimetype": mimetype, "data": data, "ext": ext})
        except:
            raise ImageProcessingError()
