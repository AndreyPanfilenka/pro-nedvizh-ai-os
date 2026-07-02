from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    ROOM = "room"
    HOUSE = "house"
    TOWNHOUSE = "townhouse"
    LAND = "land"
    COMMERCIAL = "commercial"
    GARAGE = "garage"
    OTHER = "other"


class DealType(str, Enum):
    SALE = "sale"
    RENT = "rent"
    DAILY_RENT = "daily_rent"


class Property(BaseModel):
    title: str
    price: float | None = None
    currency: str | None = None
    city: str | None = None
    district: str | None = None
    address: str | None = None
    rooms: int | None = None
    floor: int | None = None
    total_area: float | None = None
    living_area: float | None = None
    kitchen_area: float | None = None
    property_type: PropertyType
    deal_type: DealType
    photos: list[str] = Field(default_factory=list)
    description_ai: str
    telegram_text: str
    instagram_text: str
    reels_script: str
    quality_score: int = Field(ge=0, le=100)


class ProcessUrlRequest(BaseModel):
    source_url: HttpUrl


class ProcessUrlResponse(BaseModel):
    status: Literal["success"] = "success"
    property: Property
