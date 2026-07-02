from __future__ import annotations

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.models.source_content import SourceContent
from app.utils.logger import get_logger

logger = get_logger(__name__)

REMOVABLE_TAGS = (
    "script",
    "style",
    "noscript",
    "nav",
    "footer",
    "header",
    "aside",
    "iframe",
    "svg",
)

REMOVABLE_SELECTORS = (
    "[role='navigation']",
    "[role='contentinfo']",
    "[role='banner']",
    ".nav",
    ".navbar",
    ".footer",
    ".site-footer",
    ".header",
    ".site-header",
    ".cookie",
    ".cookies",
    ".advertisement",
    ".ads",
)


class ContentExtractorError(Exception):
    """Raised when page content cannot be extracted."""


class ContentExtractor:
    """Extracts readable text and metadata from listing HTML."""

    def extract(self, source_url: str, html: str) -> SourceContent:
        """Parse HTML and return structured source content."""
        if not html.strip():
            raise ContentExtractorError("HTML content is empty")

        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception as exc:
            raise ContentExtractorError(f"Failed to parse HTML: {exc}") from exc

        domain = self._extract_domain(source_url)
        title = self._extract_title(soup)
        description = self._extract_description(soup)
        images = self._extract_images(soup, source_url)
        text = self._extract_text(soup)

        logger.info(
            "Extracted content: domain=%s title=%r text_len=%s images=%s",
            domain,
            title,
            len(text),
            len(images),
        )

        return SourceContent(
            url=source_url,
            domain=domain,
            title=title,
            description=description,
            text=text,
            images=images,
        )

    def _extract_domain(self, source_url: str) -> str:
        parsed = urlparse(source_url)
        return parsed.netloc or ""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()

        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            return title_tag.string.strip()

        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        for attr, value in (
            ("property", "og:description"),
            ("name", "description"),
            ("name", "twitter:description"),
        ):
            tag = soup.find("meta", attrs={attr: value})
            if tag and tag.get("content"):
                return tag["content"].strip()

        return ""

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        seen: set[str] = set()
        images: list[str] = []

        for tag in soup.find_all("img"):
            for attr in ("src", "data-src", "data-lazy-src", "data-original"):
                raw = tag.get(attr)
                if not raw:
                    continue

                absolute = urljoin(base_url, raw.strip())
                if absolute.startswith(("http://", "https://")) and absolute not in seen:
                    seen.add(absolute)
                    images.append(absolute)

        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            absolute = urljoin(base_url, og_image["content"].strip())
            if absolute.startswith(("http://", "https://")) and absolute not in seen:
                images.insert(0, absolute)

        return images

    def _extract_text(self, soup: BeautifulSoup) -> str:
        working = BeautifulSoup(str(soup), "html.parser")

        for tag_name in REMOVABLE_TAGS:
            for tag in working.find_all(tag_name):
                tag.decompose()

        for selector in REMOVABLE_SELECTORS:
            for tag in working.select(selector):
                tag.decompose()

        main = working.find("main") or working.find("article") or working.body
        if main is None:
            return ""

        lines = [
            line.strip()
            for line in main.get_text("\n", strip=True).splitlines()
            if line.strip()
        ]
        return "\n".join(lines)
