import typer
import sys
import os
from typing import Optional
from domain.schemas import InvalidImage, ImageProcessingError
from domain.image_service import ImageService
from application.image_parser import ImageParserAdapter
from application.image_processor import ImageProcessorAdapter
from application.image_processor_opencv import ImageProcessorOpenCV

cv_service = ImageService(ImageParserAdapter(), ImageProcessorOpenCV())
ml_service = ImageService(ImageParserAdapter(), ImageProcessorAdapter())


def process(
    data: Optional[typer.FileBinaryRead] = typer.Option(
        None, help="El binario de la imagen"
    ),
    operator: int = typer.Option(
        1, help="El operador que va a procesar la imagen (1 o 2)."
    ),
    path: Optional[str] = typer.Option(None, help="La ubicación de la imagen"),
    out: Optional[str] = typer.Option(
        "processed",
        help="El nombre del archivo de salida (sin extensión) o (-) para el stdout",
    ),
):
    service: ImageService
    if operator == 1:
        service = cv_service
    else:
        service = ml_service

    try:
        if data:
            result = service.remove_background(data)
        elif path:
            result = service.remove_background(path)
        else:
            raise InvalidImage
        if not out:
            out = "processed"
        if out == "-":
            sys.stdout.buffer.write(result["data"])
            sys.stdout.flush()
            return
        else:
            out_dir = os.path.join(os.getcwd(), out + result["ext"])
            with open(out_dir, "wb") as f:
                f.write(result["data"])
                sys.stdout.write(out_dir)
    except InvalidImage as e:
        print("Imagen inválida", file=sys.stderr)
    except ImageProcessingError as e:
        print("Error al procesar la imagen", file=sys.stderr)


if __name__ == "__main__":
    typer.run(process)
