from fastapi import FastAPI, HTTPException

from app.config import APP_NAME
from app.models.property import ProcessUrlRequest, ProcessUrlResponse
from app.models.source_content import ExtractUrlRequest, ExtractUrlResponse
from app.services.property_processor import PropertyProcessor, PropertyProcessorError
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(
    title=APP_NAME,
    description="Backend core for real estate URL parsing via OpenRouter",
    version="0.1.0",
)

processor = PropertyProcessor()


@app.get("/health")
async def health() -> dict[str, str]:
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
