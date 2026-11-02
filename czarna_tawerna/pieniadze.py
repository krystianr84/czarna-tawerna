"""Kwoty w groszach (int) - bez błędów zaokrągleń typu float."""


def pln(kwota_zl: float) -> int:
    """Zamienia złote na grosze, np. pln(14) -> 1400."""
    return round(kwota_zl * 100)


def format_pln(grosze: int) -> str:
    """Formatuje grosze jako kwotę w złotych, np. 1450 -> '14,50 zł'."""
    zlote, reszta = divmod(abs(grosze), 100)
    znak = "-" if grosze < 0 else ""
    if reszta == 0:
        return f"{znak}{zlote} zł"
    return f"{znak}{zlote},{reszta:02d} zł"
