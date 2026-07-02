from __future__ import annotations

import requests

from app.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT_SECONDS = 30

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


class UrlFetcherError(Exception):
    """Raised when fetching a URL fails."""


class UrlFetcher:
    """Fetches HTML content from listing pages."""

    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    def fetch(self, source_url: str) -> str:
        """Fetch page HTML for the given URL."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        logger.info("Fetching URL: %s", source_url)

        try:
            response = requests.get(
                source_url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True,
            )
        except requests.Timeout as exc:
            raise UrlFetcherError(
                f"Request timed out after {self.timeout}s: {source_url}"
            ) from exc
        except requests.RequestException as exc:
            raise UrlFetcherError(f"Failed to fetch URL: {exc}") from exc

        if response.status_code != 200:
            raise UrlFetcherError(
                f"URL returned HTTP {response.status_code}: {source_url}"
            )

        if not response.text:
            raise UrlFetcherError(f"URL returned empty response: {source_url}")

        logger.info(
            "Fetched URL successfully: %s (status=%s, bytes=%s)",
            source_url,
            response.status_code,
            len(response.content),
        )
        return response.text
