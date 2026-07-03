from __future__ import annotations

from enum import Enum
from typing import List, Literal, Optional

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
    price: Optional[float] = None
    currency: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None
    total_area: Optional[float] = None
    living_area: Optional[float] = None
    kitchen_area: Optional[float] = None
    property_type: PropertyType
    deal_type: DealType
    photos: List[str] = Field(default_factory=list)
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
