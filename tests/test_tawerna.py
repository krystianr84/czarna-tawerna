import pytest


def test_dodanie_do_koszyka_po_id_pozycji(tawerna):
    wpis = tawerna.add_to_cart("grog_bosmana", 3)
    assert wpis.pozycja.nazwa == "Grog Bosmana"
    assert tawerna.koszyk.pozycje == [wpis]
    assert tawerna.koszyk.total() == 3 * 1400


def test_dodanie_nieistniejacej_pozycji_nie_zmienia_koszyka(tawerna):
    with pytest.raises(KeyError):
        tawerna.add_to_cart("nie_ma_takiej")
    assert tawerna.koszyk.is_empty()
