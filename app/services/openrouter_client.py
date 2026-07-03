from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests

from app.config import (
    APP_NAME,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OPENROUTER_TIMEOUT,
)
from app.models.source_content import SourceContent
from app.utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are the PRO Nedvizh property parser. The user message contains extracted page content from a real estate listing URL (source_url, title, description, text, images). Extract or infer property facts from that content and generate marketing content for PRO Nedvizh (Russian real estate, professional tone).

Return ONLY valid JSON. No markdown. No code fences. No commentary.
Use null for unknown scalar fields. Use [] for empty photos.
Do not add keys outside the schema.

Return exactly this object shape:
{
  "title": "string",
  "price": "number|null",
  "currency": "string|null",
  "city": "string|null",
  "district": "string|null",
  "address": "string|null",
  "rooms": "integer|null",
  "floor": "integer|null",
  "total_area": "number|null",
  "living_area": "number|null",
  "kitchen_area": "number|null",
  "property_type": "apartment|room|house|townhouse|land|commercial|garage|other",
  "deal_type": "sale|rent|daily_rent",
  "photos": ["string"],
  "description_ai": "string",
  "telegram_text": "string",
  "instagram_text": "string",
  "reels_script": "string",
  "quality_score": "integer"
}"""


class OpenRouterError(Exception):
    """Raised when the OpenRouter API call fails or returns an invalid payload."""


class OpenRouterClient:
    """Client for OpenRouter Chat Completions API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else OPENROUTER_API_KEY
        self.model = model or OPENROUTER_MODEL
        self.base_url = (base_url or OPENROUTER_BASE_URL).rstrip("/")
        self.timeout = timeout or OPENROUTER_TIMEOUT

    def parse_property_content(self, source: SourceContent) -> Dict[str, Any]:
        """
        Send extracted listing page content to OpenRouter and return the parsed property dict.

        Uses Chat Completions with JSON response format.
        """
        if not self.api_key:
            raise OpenRouterError("OPENROUTER_API_KEY is not configured")

        user_content = self._format_source_content(source)

        payload = {
            "model": self.model,
            "temperature": 0.2,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pro-nedvizh.ai",
            "X-Title": APP_NAME,
        }

        url = f"{self.base_url}/chat/completions"
        logger.info(
            "Calling OpenRouter model=%s for url=%s",
            self.model,
            source.url,
        )

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OpenRouterError(f"OpenRouter request failed: {exc}") from exc

        if not response.ok:
            raise OpenRouterError(
                f"OpenRouter returned HTTP {response.status_code}: {response.text}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise OpenRouterError("OpenRouter returned non-JSON response") from exc

        return self._extract_property_dict(body)

    def _extract_property_dict(self, body: Dict[str, Any]) -> Dict[str, Any]:
        choices = body.get("choices")
        if not choices:
            raise OpenRouterError("OpenRouter response missing 'choices'")

        message = choices[0].get("message", {})
        content = message.get("content")
        if not content:
            raise OpenRouterError("OpenRouter response missing message content")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise OpenRouterError(
                f"OpenRouter returned invalid JSON content: {exc}"
            ) from exc

        if not isinstance(parsed, dict):
            raise OpenRouterError("OpenRouter JSON content must be an object")

        logger.info("OpenRouter response parsed successfully")
        return parsed

    def _format_source_content(self, source: SourceContent) -> str:
        images_block = "\n".join(f"- {image}" for image in source.images[:20])
        if not images_block:
            images_block = "- (none)"

        return (
            f"Source URL: {source.url}\n"
            f"Domain: {source.domain}\n"
            f"Page title: {source.title or '(empty)'}\n"
            f"Meta description: {source.description or '(empty)'}\n"
            f"Image URLs:\n{images_block}\n\n"
            f"Page text:\n{source.text or '(empty)'}"
        )
