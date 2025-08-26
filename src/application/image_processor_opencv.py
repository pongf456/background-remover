from domain.schemas import BaseImage, ImageProcessor, InvalidImage
import cv2
import numpy as np
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))


class ImageProcessorOpenCV(ImageProcessor):
    def __edge_detection__(self, data: np.ndarray):
        blurred_float = data.astype(np.float32) / 255.0
        edgeDetector = cv2.ximgproc.createStructuredEdgeDetection(
            path.join(BASE_DIR, "../assets/model.yml")
        )
        edges = edgeDetector.detectEdges(blurred_float) * 255.0
        return edges

    def __filterOutSaltPepperNoise__(self, edgeImg):
        count = 0
        lastMedian = edgeImg
        median = cv2.medianBlur(edgeImg, 3)
        while not np.array_equal(lastMedian, median):
            zeroed = np.invert(np.logical_and(median, edgeImg))
            edgeImg[zeroed] = 0
            count = count + 1
            if count > 50:
                break
            lastMedian = median
            median = cv2.medianBlur(edgeImg, 3)

    def __findLargestContours__(self, edgeImg: np.ndarray) -> list[np.ndarray]:
        contours, hierarchy = cv2.findContours(
            edgeImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        CONTOUR_COUNT_THRESHOLD = 20

        height, width = edgeImg.shape
        total_image_area = height * width
        MIN_AREA_THRESHOLD = total_image_area * 0.001

        if len(contours) > CONTOUR_COUNT_THRESHOLD:
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                return [largest_contour]
            else:
                return []

        else:
            valid_contours = [
                c for c in contours if cv2.contourArea(c) > MIN_AREA_THRESHOLD
            ]
            return valid_contours

    def process(self, image: BaseImage) -> BaseImage:
        data = np.frombuffer(image["data"], dtype=np.uint8)
        image_opened = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if image_opened is None:
            raise InvalidImage()
        blurred_image = cv2.GaussianBlur(image_opened, (5, 5), 0)
        edged_image = self.__edge_detection__(blurred_image)
        edges_8u = np.asarray(edged_image, np.uint8)
        self.__filterOutSaltPepperNoise__(edges_8u)
        contours = self.__findLargestContours__(edges_8u)
        contourImg = np.copy(image_opened)
        cv2.drawContours(
            contourImg, contours, 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1
        )
        mask = np.zeros_like(edges_8u)
        cv2.fillPoly(mask, contours, 255)

        mapFg = cv2.erode(mask, np.ones((5, 5), np.uint8), iterations=10)

        trimap = np.copy(mask)
        trimap[mask == 0] = cv2.GC_BGD
        trimap[mask == 255] = cv2.GC_PR_BGD
        trimap[mapFg == 255] = cv2.GC_FGD

        trimap_print = np.copy(trimap)
        trimap_print[trimap_print == cv2.GC_PR_BGD] = 128
        trimap_print[trimap_print == cv2.GC_FGD] = 255
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (0, 0, mask.shape[0] - 1, mask.shape[1] - 1)
        cv2.grabCut(
            image_opened, trimap, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK
        )

        mask2 = np.where(
            (trimap == cv2.GC_FGD) | (trimap == cv2.GC_PR_FGD), 255, 0
        ).astype("uint8")
        contours2 = self.__findLargestContours__(mask2)
        mask3 = np.zeros_like(mask2)
        cv2.fillPoly(mask3, contours2, 255)
        mask3 = np.repeat(mask3[:, :, np.newaxis], 3, axis=2)
        mask4 = cv2.GaussianBlur(mask3, (3, 3), 0)
        alpha = mask4.astype(float) / 255.0

        foreground = image_opened.astype(float)

        foreground_blended = cv2.multiply(alpha, foreground)
        background_blended = cv2.multiply(
            1.0 - alpha, np.ones_like(foreground, dtype=float) * 255.0
        )
        cutout = cv2.add(foreground_blended, background_blended)

        cutout_8u = np.clip(cutout, 0, 255).astype(np.uint8)
        _, buffer = cv2.imencode(image["ext"], cutout_8u)
        return {
            "ext": image["ext"],
            "data": bytearray(buffer.tobytes()),
            "mimetype": image["mimetype"],
        }
