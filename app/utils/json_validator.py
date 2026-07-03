from typing import Tuple

REQUIRED_FIELDS: Tuple[str, ...] = (
    "title",
    "price",
    "currency",
    "city",
    "district",
    "address",
    "rooms",
    "floor",
    "total_area",
    "living_area",
    "kitchen_area",
    "property_type",
    "deal_type",
    "photos",
    "description_ai",
    "telegram_text",
    "instagram_text",
    "reels_script",
    "quality_score",
)


class JsonValidationError(ValueError):
    """Raised when parsed OpenRouter JSON is missing required fields."""


def validate_required_fields(data: dict) -> None:
    """Ensure all required property fields are present in the parsed JSON object."""
    if not isinstance(data, dict):
        raise JsonValidationError("Response must be a JSON object")

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise JsonValidationError(
            f"Missing required fields: {', '.join(sorted(missing))}"
        )
