"""Klasy opisujące menu tawerny."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MenuItem(ABC):
    """Pojedyncza pozycja w karcie.

    Klasa abstrakcyjna - konkretne są Drink i Dish.
    """

    id: str
    nazwa: str
    opis: str
    cena: int  # w groszach
    kategoria_id: str
    oznaczenia: frozenset[str] = frozenset()

    @abstractmethod
    def kind(self) -> str:
        """Rodzaj pozycji do wyświetlenia klientowi, np. „napój”."""

    def price(self) -> int:
        """Cena pozycji w groszach."""
        return self.cena


@dataclass(frozen=True)
class Drink(MenuItem):
    def kind(self) -> str:
        return "napój"


@dataclass(frozen=True)
class Dish(MenuItem):
    def kind(self) -> str:
        return "danie"


@dataclass
class Category:
    id: str
    nazwa: str
    pozycje: list[MenuItem] = field(default_factory=list)


@dataclass
class Menu:
    kategorie: list[Category] = field(default_factory=list)

    def all_items(self) -> list[MenuItem]:
        return [p for k in self.kategorie for p in k.pozycje]

    def item(self, id_pozycji: str) -> MenuItem:
        for p in self.all_items():
            if p.id == id_pozycji:
                return p
        raise KeyError(f"Brak pozycji o id {id_pozycji!r}")
