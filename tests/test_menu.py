import json
from dataclasses import dataclass

import pytest

from czarna_tawerna.menu import Dish, Drink, MenuItem, MenuItemFactory, load_menu
from czarna_tawerna.pieniadze import format_pln, pln


def test_menu_ma_piec_kategorii_i_25_pozycji(menu):
    assert len(menu.kategorie) == 5
    assert len(menu.all_items()) == 25


def test_fabryka_tworzy_wlasciwy_typ(menu):
    assert isinstance(menu.item("latte_bosmana"), Drink)
    assert isinstance(menu.item("tost_kartografa"), Dish)


def test_fabryka_przepisuje_dane_pozycji():
    pozycja = MenuItemFactory().create(
        {"id": "grog", "typ": "napoj", "nazwa": "Grog", "opis": "korzenny", "cena": 14,
         "oznaczenia": ["wege"]}, "tortuga")
    assert (pozycja.id, pozycja.nazwa, pozycja.opis, pozycja.kategoria_id) == \
        ("grog", "Grog", "korzenny", "tortuga")
    assert pozycja.price() == 1400
    assert pozycja.oznaczenia == {"wege"}


def test_fabryka_odrzuca_nieznany_typ():
    with pytest.raises(ValueError, match="statek"):
        MenuItemFactory().create({"id": "x", "typ": "statek", "nazwa": "X", "cena": 1}, "kawy")


def test_fabryka_przyjmuje_nowy_typ_pozycji_przez_rejestracje():
    # nowy rodzaj pozycji: nowa klasa + register(), fabryka bez zmian
    @dataclass(frozen=True)
    class ComboMeal(Dish):
        def kind(self) -> str:
            return "zestaw"

    fabryka = MenuItemFactory()
    fabryka.register("zestaw", lambda dane, kategoria_id: ComboMeal(
        id=dane["id"], nazwa=dane["nazwa"], opis="", cena=pln(dane["cena"]),
        kategoria_id=kategoria_id))
    zestaw = fabryka.create({"id": "zestaw_kapitana", "typ": "zestaw", "nazwa": "Zestaw Kapitana",
                             "cena": 25}, "zestawy")
    assert isinstance(zestaw, ComboMeal)
    assert (zestaw.kind(), zestaw.price()) == ("zestaw", 2500)
    # wbudowane typy nadal działają
    napoj = fabryka.create({"id": "x", "typ": "napoj", "nazwa": "X", "cena": 1}, "kawy")
    assert isinstance(napoj, Drink)


def test_nowa_kategoria_i_danie_wymagaja_tylko_zmiany_pliku_menu(tmp_path):
    plik = tmp_path / "menu.json"
    plik.write_text(json.dumps({"kategorie": [
        {"id": "zupy", "nazwa": "Zupy z kotła", "pozycje": [
            {"id": "zupa_rybna", "typ": "danie", "nazwa": "Zupa Rybna", "cena": 18},
        ]},
    ]}), encoding="utf-8")
    menu = load_menu(plik)
    assert [k.nazwa for k in menu.kategorie] == ["Zupy z kotła"]
    assert menu.item("zupa_rybna").price() == 1800


def test_pozycji_menu_nie_da_sie_utworzyc_bezposrednio():
    with pytest.raises(TypeError):
        MenuItem("x", "X", "", 100, "kawy")


def test_rodzaj_pozycji_zalezy_od_klasy(menu):
    assert menu.item("latte_bosmana").kind() == "napój"
    assert menu.item("sernik_gubernatora").kind() == "danie"


def test_brak_pozycji_o_podanym_id(menu):
    with pytest.raises(KeyError):
        menu.item("nie_ma_takiej")


@pytest.mark.parametrize("grosze, tekst", [(900, "9 zł"), (1450, "14,50 zł"), (-300, "-3 zł")],
                         ids=["pelne_zlote", "z_groszami", "ujemna"])
def test_format_pln(grosze, tekst):
    assert format_pln(grosze) == tekst
