from src.tournaments.utils.site_block_text import get_plain_block_text

CREDIT_MARKER = 'data-developer-credit="prometeylabs"'
CREDIT_URL = "https://www.prometeylabs.com/"
CREDIT_NAME = "PrometeyLabs"


def credit_text() -> str:
    return get_plain_block_text("footer", "dev_credit_text", fallback="Сайт розроблено")


def credit_html() -> str:
    return (
        f'<div class="site-footer__credit" {CREDIT_MARKER}>'
        f"{credit_text()} "
        f'<a href="{CREDIT_URL}" class="site-footer__credit-link" '
        f'rel="noopener noreferrer" target="_blank">{CREDIT_NAME}</a>'
        f"</div>"
    )


def credit_is_present(content: str) -> bool:
    return CREDIT_MARKER in content
