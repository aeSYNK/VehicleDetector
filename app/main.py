import base64
import io

from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.models import process_image, VehicleDetectionResult
from app.schemas import VehicleImageResponse

app = FastAPI(title="Vehicle Detection API")


@app.post("/detect-vehicles/", response_model=VehicleImageResponse)
async def detect_vehicles(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Чтение изображения
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Обработка изображения
        result: VehicleDetectionResult = process_image(image)

        # Подготовка ответа
        vehicles = []
        for idx, (vehicle_img, label) in enumerate(
                zip(result.vehicle_images, result.labels)
        ):
            img_byte_arr = io.BytesIO()
            vehicle_img.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)

            encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode(
                'utf-8'
            )
            vehicles.append(
                {
                    "name": label,
                    "image": f"data:image/jpeg;base64,{encoded_image}"
                }
            )

        return {
            "vehicle_count": len(vehicles),
            "vehicles": vehicles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
