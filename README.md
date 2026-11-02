# 🏴‍☠️ Czarna Tawerna

System zamówień w pirackiej tawernie - projekt semestralny z przedmiotu **Programowanie obiektowe II** (Akademia Humanistyczno-Ekonomiczna w Łodzi, Informatyka, rok akademicki 2026/2027).

Aplikacja działa jak kiosk samoobsługowy. Na etapie 2 klient przegląda menu podzielone na kategorie, dodaje pozycje do koszyka, usuwa je i widzi wartość koszyka. W kolejnych etapach dojdą m.in. rozmiary („Szalupa / Bryg / Galeon”), dodatki („łupy”), promocje i składanie zamówienia ze śledzeniem statusu.

> **Status:** etap 2 - menu i koszyk.

Nazwy klas, metod i funkcji są po angielsku (PEP 8), a pozostałe nazwy, komentarze i teksty interfejsu - po polsku.

## Załoga

| Osoba | Nr albumu | Rola | Zakres | Wzorce |
|---|---|---|---|---|
| Krystian Rutkowski (Szyper) | 167040 | kierownik, interfejs i integracja | `interfejs/`, `app.py` | Observer |
| Katarzyna Pater (Kwatermistrz) | 167683 | zamówienia | `zamowienia/` | Strategy, Observer |
| Dariusz Lorenz (Kuk) | 167014 | personalizacja (od kolejnego etapu; w etapie 2 - diagram klas) | `personalizacja/` (w poczekalni) | Decorator |
| Wiktor Purgał (Nawigator) | 165328 | menu | `menu/` | Fabryka |

## Technologia

- Python 3.10+
- [Streamlit](https://streamlit.io/) - interfejs graficzny
- pytest - testy jednostkowe
- fpdf2 - pliki PDF (paragon - planowany)

## Uruchomienie

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py   # aplikacja
pytest                 # testy
```

Bez aktywacji środowiska (np. w zwykłym terminalu poza PyCharmem) aplikację uruchamia skrypt `.\uruchom.ps1` - korzysta z Pythona w `.venv` i działa z dowolnego folderu.

Pojedynczy plik lub test: `pytest tests/test_zamowienia.py` lub `pytest -k nazwa_testu`.

Sprawdzenie stylu PEP 8 (narzędzie spoza `requirements.txt`, konfiguracja w `setup.cfg`):

```powershell
pip install pycodestyle
pycodestyle czarna_tawerna app.py tests
```

## Struktura projektu

```
app.py                  interfejs Streamlit (tylko prezentacja)
dane/menu.json          menu: kategorie i pozycje z cenami
dane/zdjecia/           grafiki poglądowe pozycji (<id>.jpg, wygenerowane AI), brak.jpg, pochodzenie w ZRODLA.md
czarna_tawerna/
  pieniadze.py          kwoty w groszach (int) i formatowanie „14,50 zł”
  menu/                 model menu, wczytywanie z JSON, fabryka pozycji
  zamowienia/           koszyk
  interfejs/            klasa Tavern (stan sesji kiosku)
tests/                  testy pytest
specs/czarna-tawerna/   specyfikacja SDD: requirements.md, design.md, tasks.md
sprawozdanie/           generator sprawozdania DOCX
req/                    instrukcje etapów od prowadzącego
```

Logika w pakiecie `czarna_tawerna` nie zależy od Streamlita - `app.py` korzysta z niej przez klasę `Tavern`.

## Wzorce projektowe

| Wzorzec | Gdzie | Zastosowanie |
|---|---|---|
| Fabryka (fabryka prosta z rejestrem typów) | `menu/fabryka.py` | tworzenie pozycji menu (napój, danie) na podstawie pola `typ` z pliku; nowe rodzaje pozycji przez `register()` |

Kolejne etapy: Decorator (dodatki do produktu), Strategy (promocje) i Observer (powiadomienia o statusie zamówienia).

## Specyfikacja (Spec-Driven Development)

Projekt prowadzimy metodą Spec-Driven Development. W katalogu `specs/czarna-tawerna/` są trzy pliki, które czyta się po kolei:

1. [`requirements.md`](specs/czarna-tawerna/requirements.md) - wymagania (historyjki użytkownika i kryteria akceptacji),
2. [`design.md`](specs/czarna-tawerna/design.md) - projekt: architektura, klasy, wzorce, diagramy,
3. [`tasks.md`](specs/czarna-tawerna/tasks.md) - lista zadań z podziałem na osoby.

Najpierw zmieniamy specyfikację, potem kod.

## Sprawozdanie

Sprawozdanie generuje skrypt `sprawozdanie/generuj_sprawozdanie.py` (plik wynikowy `sprawozdanie/programowanie2_sprawozdanie.docx`, nadpisywany tylko z opcją `--nadpisz`).

## Oddawanie

Od etapu 2 oddaje się archiwum ZIP z kodem i sprawozdaniem - **bez** `.venv/`, `__pycache__/` i `.pytest_cache/`.
