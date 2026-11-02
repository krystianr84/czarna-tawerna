"""Stan jednej sesji kiosku: menu i koszyk."""

from __future__ import annotations

from pathlib import Path

from ..menu import Menu, load_menu
from ..zamowienia import Cart, CartItem


class Tavern:
    def __init__(self, plik_menu: Path) -> None:
        self.menu: Menu = load_menu(plik_menu)
        self.koszyk = Cart()

    def add_to_cart(self, id_pozycji: str, ilosc: int = 1) -> CartItem:
        """Dodaje do koszyka pozycję menu o podanym id."""
        return self.koszyk.add(self.menu.item(id_pozycji), ilosc)
