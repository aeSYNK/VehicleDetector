from pydantic import BaseModel
from typing import List

class VehicleImage(BaseModel):
    name: str
    image: str  # base64 encoded image with data URI prefix

class VehicleImageResponse(BaseModel):
    vehicle_count: int
    vehicles: List[VehicleImage]
