from pathlib import Path

import pytest

from czarna_tawerna.interfejs import Tavern
from czarna_tawerna.menu import Menu, load_menu

PLIK_MENU = Path(__file__).parent.parent / "dane" / "menu.json"


@pytest.fixture
def menu() -> Menu:
    return load_menu(PLIK_MENU)


@pytest.fixture
def tawerna() -> Tavern:
    return Tavern(PLIK_MENU)
