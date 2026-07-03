from __future__ import annotations

import json
from typing import Any, Dict, Optional, Tuple

import requests
from pydantic import ValidationError

from app.config import (
    APP_NAME,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OPENROUTER_TIMEOUT,
)
from app.models.property import Property
from app.models.publication import Publication
from app.utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are the content editor for PRO Nedvizh — агентство недвижимости в Беларуси.

Создай готовые к публикации материалы для объявления о недвижимости на основе переданных данных.

Регион: Мозырь, Калинковичи, Наровля, Ельск и близлежащие населённые пункты.
Язык: русский.
Стиль: профессиональный, полезный, без кликбейта и преувеличений.
Бренд: PRO Nedvizh — упоминай аккуратно, без навязчивой рекламы.

Требования к контенту:
- title: короткий цепляющий заголовок (до 80 символов), отражает суть объекта
- telegram_text: пост для Telegram — структурированный, с ключевыми параметрами, эмодзи умеренно, призыв связаться с PRO Nedvizh
- instagram_text: пост для Instagram — живой, но деловой тон, абзацы, призыв к действию
- reels_script: сценарий короткого Reels (30–45 сек), с таймкодами и текстом закадрового голоса
- hashtags: 8–15 релевантных хештегов на русском и английском (без # в значениях)

Return ONLY valid JSON. No markdown. No code fences. No commentary.

Return exactly this object shape:
{
  "title": "string",
  "telegram_text": "string",
  "instagram_text": "string",
  "reels_script": "string",
  "hashtags": ["string"]
}"""

PUBLICATION_REQUIRED_FIELDS: Tuple[str, ...] = (
    "title",
    "telegram_text",
    "instagram_text",
    "reels_script",
    "hashtags",
)


class PublicationGeneratorError(Exception):
    """Raised when publication generation fails."""


class PublicationGenerator:
    """Generates ready-to-publish social media content from a normalized Property."""

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

    def generate(self, property_obj: Property) -> Publication:
        """Call OpenRouter and return validated Publication content."""
        raw_data = self._call_openrouter(property_obj)

        missing = [
            field for field in PUBLICATION_REQUIRED_FIELDS if field not in raw_data
        ]
        if missing:
            raise PublicationGeneratorError(
                f"Missing required publication fields: {', '.join(sorted(missing))}"
            )

        try:
            publication = Publication.model_validate(raw_data)
        except ValidationError as exc:
            raise PublicationGeneratorError(
                f"Publication data failed schema validation: {exc}"
            ) from exc

        logger.info("Publication generated: title=%r", publication.title)
        return publication

    def _call_openrouter(self, property_obj: Property) -> Dict[str, Any]:
        if not self.api_key:
            raise PublicationGeneratorError("OPENROUTER_API_KEY is not configured")

        user_content = self._format_property(property_obj)

        payload = {
            "model": self.model,
            "temperature": 0.4,
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
            "Generating publication via OpenRouter model=%s for property=%r",
            self.model,
            property_obj.title,
        )

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise PublicationGeneratorError(
                f"OpenRouter request failed: {exc}"
            ) from exc

        if not response.ok:
            raise PublicationGeneratorError(
                f"OpenRouter returned HTTP {response.status_code}: {response.text}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise PublicationGeneratorError(
                "OpenRouter returned non-JSON response"
            ) from exc

        return self._extract_json_dict(body)

    def _extract_json_dict(self, body: Dict[str, Any]) -> Dict[str, Any]:
        choices = body.get("choices")
        if not choices:
            raise PublicationGeneratorError("OpenRouter response missing 'choices'")

        message = choices[0].get("message", {})
        content = message.get("content")
        if not content:
            raise PublicationGeneratorError(
                "OpenRouter response missing message content"
            )

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise PublicationGeneratorError(
                f"OpenRouter returned invalid JSON content: {exc}"
            ) from exc

        if not isinstance(parsed, dict):
            raise PublicationGeneratorError("OpenRouter JSON content must be an object")

        return parsed

    def _format_property(self, property_obj: Property) -> str:
        photos_block = "\n".join(f"- {photo}" for photo in property_obj.photos[:10])
        if not photos_block:
            photos_block = "- (нет фото)"

        price_line = (
            f"{property_obj.price} {property_obj.currency}"
            if property_obj.price is not None
            else "не указана"
        )

        return (
            f"Заголовок: {property_obj.title}\n"
            f"Цена: {price_line}\n"
            f"Город: {property_obj.city or '(не указан)'}\n"
            f"Район: {property_obj.district or '(не указан)'}\n"
            f"Адрес: {property_obj.address or '(не указан)'}\n"
            f"Комнат: {property_obj.rooms if property_obj.rooms is not None else '(не указано)'}\n"
            f"Этаж: {property_obj.floor if property_obj.floor is not None else '(не указан)'}\n"
            f"Общая площадь: {property_obj.total_area if property_obj.total_area is not None else '(не указана)'} м²\n"
            f"Жилая площадь: {property_obj.living_area if property_obj.living_area is not None else '(не указана)'} м²\n"
            f"Площадь кухни: {property_obj.kitchen_area if property_obj.kitchen_area is not None else '(не указана)'} м²\n"
            f"Тип объекта: {property_obj.property_type.value}\n"
            f"Тип сделки: {property_obj.deal_type.value}\n"
            f"Описание: {property_obj.description_ai}\n"
            f"Фото:\n{photos_block}"
        )
