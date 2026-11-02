"""Wzorzec Fabryka (fabryka prosta z rejestrem typów).

Tworzy pozycje menu na podstawie danych z pliku.
"""

from __future__ import annotations

from typing import Any, Callable

from ..pieniadze import pln
from .model import Dish, Drink, MenuItem

ItemConstructor = Callable[[dict[str, Any], str], MenuItem]


def _common_fields(dane: dict[str, Any], kategoria_id: str) -> dict[str, Any]:
    return {
        "id": dane["id"],
        "nazwa": dane["nazwa"],
        "opis": dane.get("opis", ""),
        "cena": pln(dane["cena"]),
        "kategoria_id": kategoria_id,
        "oznaczenia": frozenset(dane.get("oznaczenia", [])),
    }


def _create_drink(dane: dict[str, Any], kategoria_id: str) -> Drink:
    return Drink(**_common_fields(dane, kategoria_id))


def _create_dish(dane: dict[str, Any], kategoria_id: str) -> Dish:
    return Dish(**_common_fields(dane, kategoria_id))


class MenuItemFactory:
    """Tworzy właściwy obiekt pozycji na podstawie pola „typ”.

    Nowy rodzaj pozycji dodaje się przez register(), bez zmiany
    kodu fabryki (Open/Closed).
    """

    def __init__(self) -> None:
        self._konstruktory: dict[str, ItemConstructor] = {
            "napoj": _create_drink,
            "danie": _create_dish,
        }

    def register(self, typ: str, konstruktor: ItemConstructor) -> None:
        self._konstruktory[typ] = konstruktor

    def create(self, dane: dict[str, Any], kategoria_id: str) -> MenuItem:
        typ = dane.get("typ")
        try:
            konstruktor = self._konstruktory[typ]
        except KeyError:
            raise ValueError(f"Nieznany typ pozycji: {typ!r}") from None
        return konstruktor(dane, kategoria_id)
