from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
from typing import List, NamedTuple


class VehicleDetectionResult(NamedTuple):
    vehicle_images: List[Image.Image]
    labels: List[str]


# Загрузка модели
model = None


def load_model():
    global model
    if model is None:
        model = YOLO("yolov8n-seg.pt")
    return model


def process_image(image: Image.Image) -> VehicleDetectionResult:
    model = load_model()

    vehicle_classes = {
        1: "bicycle",
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck"
    }

    results = model(image)

    vehicle_images = []
    labels = []

    for result in results:
        for box, mask, cls in zip(
                result.boxes, result.masks, result.boxes.cls
        ):
            if int(cls) in vehicle_classes:
                label = vehicle_classes[int(cls)]
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Добавляем отступ вокруг объекта подписи
                padding = 0
                x1 = max(0, x1 - padding)
                y1 = max(0, y1 - padding)
                x2 = min(image.width, x2 + padding)
                y2 = min(image.height, y2 + padding)

                # Вырезаем объект
                vehicle_img = image.crop((x1, y1, x2, y2))

                # Создаем копию для добавления подписи
                labeled_img = vehicle_img.copy()
                draw = ImageDraw.Draw(labeled_img)

                try:
                    font = ImageFont.truetype("arial.ttf", 10)
                except:
                    font = ImageFont.load_default()

                # Добавляем подпись с фоном для лучшей читаемости
                text = label.upper()
                # Получаем размеры текста новым способом
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Рисуем прямоугольник фона
                draw.rectangle(
                    [(0, 0), (text_width, text_height + 5)],
                    fill="black"
                )
                # Добавляем текст
                draw.text(
                    (0, 0),
                    text,
                    fill="white",
                    font=font
                )

                vehicle_images.append(labeled_img)
                labels.append(label)

    return VehicleDetectionResult(vehicle_images, labels)
