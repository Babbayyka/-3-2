"""URL-конвертеры для приложения listings."""


class UnicodeSlugConverter:
    """Конвертер slug, поддерживающий unicode-символы (включая кириллицу).

    Стандартный django `<slug>` ограничен `[-a-zA-Z0-9_]+`, поэтому slug-и,
    сгенерированные через `slugify(..., allow_unicode=True)`, не сопоставляются
    его маршрутам и `reverse()` падает с NoReverseMatch. Этот конвертер
    использует `\\w` с включённым флагом UNICODE (поведение `re` в Python 3 по
    умолчанию), что позволяет матчить буквы любых алфавитов, цифры и `_`,
    плюс дефис.
    """

    regex = r"[-\w]+"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value
