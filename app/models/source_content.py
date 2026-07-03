from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field, HttpUrl


class SourceContent(BaseModel):
    url: HttpUrl
    domain: str
    title: str = ""
    description: str = ""
    text: str = ""
    images: List[str] = Field(default_factory=list)


class ExtractUrlRequest(BaseModel):
    source_url: HttpUrl


class ExtractUrlResponse(BaseModel):
    status: Literal["success"] = "success"
    source: SourceContent
