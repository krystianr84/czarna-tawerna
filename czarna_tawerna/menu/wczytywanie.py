"""Wczytywanie menu z pliku JSON."""

from __future__ import annotations

import json
from pathlib import Path

from .fabryka import MenuItemFactory
from .model import Category, Menu


def load_menu(sciezka: Path, fabryka: MenuItemFactory | None = None) -> Menu:
    fabryka = fabryka or MenuItemFactory()
    dane = json.loads(Path(sciezka).read_text(encoding="utf-8"))
    kategorie = [
        Category(id=kat["id"], nazwa=kat["nazwa"],
                 pozycje=[fabryka.create(p, kat["id"]) for p in kat["pozycje"]])
        for kat in dane["kategorie"]
    ]
    return Menu(kategorie=kategorie)
