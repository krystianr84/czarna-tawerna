import pytest

from czarna_tawerna.menu import MenuItemFactory
from czarna_tawerna.pieniadze import format_pln
from czarna_tawerna.zamowienia import Cart


@pytest.fixture
def koszyk(menu) -> Cart:
    k = Cart()
    k.add(menu.item("latte_bosmana"), ilosc=2)   # 2 × 15 zł
    k.add(menu.item("sernik_gubernatora"))       # 15 zł
    return k


def test_nowy_koszyk_jest_pusty():
    k = Cart()
    assert k.is_empty()
    assert k.total() == 0


def test_suma_koszyka(koszyk):
    assert not koszyk.is_empty()
    assert [p.value() for p in koszyk.pozycje] == [3000, 1500]
    assert koszyk.total() == 4500


def test_ilosc_musi_byc_dodatnia(menu):
    with pytest.raises(ValueError):
        Cart().add(menu.item("latte_bosmana"), ilosc=0)


def test_usuniecie_pozycji_z_koszyka(koszyk):
    latte, sernik = koszyk.pozycje
    koszyk.remove(latte)
    assert koszyk.pozycje == [sernik]
    assert koszyk.total() == 1500


def test_usuniecie_pozycji_spoza_koszyka_zglasza_blad(menu, koszyk):
    obca = Cart().add(menu.item("latte_bosmana"))
    with pytest.raises(ValueError, match="nie ma w koszyku"):
        koszyk.remove(obca)
    assert len(koszyk.pozycje) == 2
    assert koszyk.total() == 4500


def test_wyczyszczenie_koszyka(koszyk):
    koszyk.clear()
    assert koszyk.is_empty()
    assert koszyk.total() == 0


def test_kwoty_liczone_dokladnie_bez_bledow_float():
    # na float 1.10 + 2.20 = 3.3000000000000003, w groszach - dokładnie
    fabryka = MenuItemFactory()
    woda = fabryka.create(
        {"id": "woda", "typ": "danie", "nazwa": "Woda", "cena": 1.10}, "test")
    suchar = fabryka.create(
        {"id": "suchar", "typ": "danie", "nazwa": "Suchar", "cena": 2.20}, "test")
    k = Cart()
    k.add(woda)
    k.add(suchar)
    assert k.total() == 330
    assert format_pln(k.total()) == "3,30 zł"
