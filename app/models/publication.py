from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl

from app.models.property import Property


class Publication(BaseModel):
    title: str
    telegram_text: str
    instagram_text: str
    reels_script: str
    hashtags: list[str]


class GeneratePublicationRequest(BaseModel):
    source_url: HttpUrl


class GeneratePublicationResponse(BaseModel):
    status: Literal["success"] = "success"
    source_url: str
    property: Property
    publication: Publication
