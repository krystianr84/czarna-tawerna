import json
from dataclasses import dataclass

import pytest

from czarna_tawerna.menu import Dish, Drink, MenuItemFactory, load_menu
from czarna_tawerna.pieniadze import pln


def test_menu_ma_piec_kategorii_i_25_pozycji(menu):
    assert len(menu.kategorie) == 5
    assert len(menu.all_items()) == 25


def test_fabryka_tworzy_wlasciwy_typ(menu):
    latte, tost = menu.item("latte_bosmana"), menu.item("tost_kartografa")
    assert isinstance(latte, Drink)
    assert isinstance(tost, Dish)
    assert (latte.kind(), tost.kind()) == ("napój", "danie")


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
