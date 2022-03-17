from country_codes import get_german_country_name_from_code


def test_get_german_country_name_from_code():
    assert get_german_country_name_from_code("de") == "Deutschland"
