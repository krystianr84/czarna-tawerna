"""Koszyk - pozycje menu wybrane przez klienta."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..menu import MenuItem


@dataclass
class CartItem:
    pozycja: MenuItem
    ilosc: int = 1

    def __post_init__(self) -> None:
        if self.ilosc < 1:
            raise ValueError("Ilość musi być dodatnia")

    def value(self) -> int:
        return self.pozycja.price() * self.ilosc


@dataclass
class Cart:
    pozycje: list[CartItem] = field(default_factory=list)

    def add(self, pozycja: MenuItem, ilosc: int = 1) -> CartItem:
        wpis = CartItem(pozycja, ilosc)
        self.pozycje.append(wpis)
        return wpis

    def remove(self, wpis: CartItem) -> None:
        # porównanie tożsamości: usuwamy tę konkretną pozycję koszyka
        for i, p in enumerate(self.pozycje):
            if p is wpis:
                del self.pozycje[i]
                return
        raise ValueError("Tej pozycji nie ma w koszyku")

    def clear(self) -> None:
        self.pozycje.clear()

    def total(self) -> int:
        return sum(p.value() for p in self.pozycje)

    def is_empty(self) -> bool:
        return not self.pozycje
