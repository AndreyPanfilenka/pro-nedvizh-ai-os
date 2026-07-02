from __future__ import annotations

from pydantic import ValidationError

from app.models.property import Property
from app.models.source_content import SourceContent
from app.services.content_extractor import ContentExtractor, ContentExtractorError
from app.services.openrouter_client import OpenRouterClient, OpenRouterError
from app.services.url_fetcher import UrlFetcher, UrlFetcherError
from app.utils.json_validator import JsonValidationError, validate_required_fields
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PropertyProcessorError(Exception):
    """Raised when property processing fails at any pipeline stage."""


class PropertyProcessor:
    """Coordinates URL fetch, content extraction, OpenRouter parsing, and normalization."""

    def __init__(
        self,
        url_fetcher: UrlFetcher | None = None,
        content_extractor: ContentExtractor | None = None,
        openrouter_client: OpenRouterClient | None = None,
    ) -> None:
        self.url_fetcher = url_fetcher or UrlFetcher()
        self.content_extractor = content_extractor or ContentExtractor()
        self.openrouter_client = openrouter_client or OpenRouterClient()

    def extract_source_content(self, source_url: str) -> SourceContent:
        """Fetch a listing URL and extract readable page content."""
        logger.info("Extracting source content from URL: %s", source_url)

        try:
            html = self.url_fetcher.fetch(source_url)
        except UrlFetcherError as exc:
            raise PropertyProcessorError(str(exc)) from exc

        try:
            return self.content_extractor.extract(source_url, html)
        except ContentExtractorError as exc:
            raise PropertyProcessorError(str(exc)) from exc

    def process_url(self, source_url: str) -> Property:
        """
        Process a listing URL end-to-end.

        1. Fetch the page HTML
        2. Extract readable content and metadata
        3. Call OpenRouter with extracted content
        4. Validate required JSON fields
        5. Normalize into a Property model for downstream Google Sheets export
        """
        source = self.extract_source_content(source_url)

        try:
            raw_data = self.openrouter_client.parse_property_content(source)
        except OpenRouterError as exc:
            raise PropertyProcessorError(str(exc)) from exc

        try:
            validate_required_fields(raw_data)
        except JsonValidationError as exc:
            raise PropertyProcessorError(str(exc)) from exc

        try:
            property_obj = Property.model_validate(raw_data)
        except ValidationError as exc:
            raise PropertyProcessorError(
                f"Property data failed schema validation: {exc}"
            ) from exc

        logger.info(
            "Property normalized: title=%r quality_score=%s",
            property_obj.title,
            property_obj.quality_score,
        )
        return property_obj
