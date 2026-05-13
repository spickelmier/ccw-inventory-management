TRANSLATIONS = {
    "en": {
        "errors": {
            "item_not_found": "Item not found",
            "order_not_found": "Order not found",
            "invalid_filter": "Invalid filter value",
            "internal_error": "Internal server error",
        }
    },
    "ja": {
        "errors": {
            "item_not_found": "アイテムが見つかりません",
            "order_not_found": "注文が見つかりません",
            "invalid_filter": "フィルター値が無効です",
            "internal_error": "内部サーバーエラー",
        }
    },
}

SUPPORTED_LOCALES = {"en", "ja"}
DEFAULT_LOCALE = "en"


def t(key: str, lang: str = "en") -> str:
    """Look up a translation key like 'errors.item_not_found' for the given lang."""
    if lang not in SUPPORTED_LOCALES:
        lang = DEFAULT_LOCALE
    keys = key.split(".")
    value = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LOCALE])
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            return key
    return value if isinstance(value, str) else key
