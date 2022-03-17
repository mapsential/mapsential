import pytest
from errors import InternationalizedTermError
from internationalized_terms import get_plural
from internationalized_terms import get_singular
from internationalized_terms import get_translation


# Term entries should really be passed as an optional parameter or mocked
# but I can't be bothered rn
def test_get_translation():
    assert "Defibrillatoren" == get_translation("defibrillators", "de")
    assert "defibrillators" == get_translation("Defibrillatoren", "en")


def test_get_translations_raises_error_without_fallback():
    with pytest.raises(InternationalizedTermError):
        get_translation(
            "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            "de",
        )


def test_get_translation_uses_fallback_if_cannot_translate():
    assert "fallback" == get_translation(
        "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
        "de",
        fallback="fallback",
    )


def test_get_plural():
    assert "Toiletten" == get_plural("Toilette")
    assert "toilets" == get_plural("toilet")


def test_get_singular():
    assert "Tafel" == get_singular("Tafeln")
    assert "soup kitchen" == get_singular("soup kitchens")
