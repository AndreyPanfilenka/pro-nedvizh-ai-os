from typing import Dict

from fastapi import FastAPI, HTTPException

from app.config import APP_NAME
from app.models.property import ProcessUrlRequest, ProcessUrlResponse
from app.models.publication import (
    GeneratePublicationRequest,
    GeneratePublicationResponse,
)
from app.models.source_content import ExtractUrlRequest, ExtractUrlResponse
from app.services.property_processor import PropertyProcessor, PropertyProcessorError
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(
    title=APP_NAME,
    description="Backend for real estate URL parsing and publication generation",
    version="0.2.0",
)

processor = PropertyProcessor()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/extract-url", response_model=ExtractUrlResponse)
async def extract_url(request: ExtractUrlRequest) -> ExtractUrlResponse:
    source_url = str(request.source_url)

    try:
        source = processor.extract_source_content(source_url)
    except PropertyProcessorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ExtractUrlResponse(status="success", source=source)


@app.post("/process-url", response_model=ProcessUrlResponse)
async def process_url(request: ProcessUrlRequest) -> ProcessUrlResponse:
    source_url = str(request.source_url)

    try:
        property_obj = processor.process_url(source_url)
    except PropertyProcessorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ProcessUrlResponse(status="success", property=property_obj)


@app.post("/generate-publication", response_model=GeneratePublicationResponse)
async def generate_publication(
    request: GeneratePublicationRequest,
) -> GeneratePublicationResponse:
    source_url = str(request.source_url)

    try:
        property_obj, publication = processor.generate_publication(source_url)
    except PropertyProcessorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return GeneratePublicationResponse(
        status="success",
        source_url=source_url,
        property=property_obj,
        publication=publication,
    )
