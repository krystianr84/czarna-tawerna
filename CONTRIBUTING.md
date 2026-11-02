# Współpraca przy projekcie Czarna Tawerna

Dziękujemy, że dokładasz cegiełkę do tawerny! Ten plik opisuje, jak pracujemy w zespole. Instalację i uruchomienie projektu opisuje [README](README.md#instalacja-i-uruchomienie).

## Kto za co odpowiada

Każda osoba ma swój obszar (pakiet) i pisze do niego testy - szczegóły w [README → Autorzy](README.md#autorzy) i w [`specs/czarna-tawerna/tasks.md`](specs/czarna-tawerna/tasks.md). Zmiany w cudzym obszarze warto najpierw uzgodnić z jego właścicielem.

## Zakres kodu = bieżący etap

W projekcie jest tylko to, czego wymaga instrukcja bieżącego etapu (teraz etap 2: menu i koszyk). Rozwiązania na kolejne etapy (rozmiary, dodatki, promocje, zamówienia ze statusami, tablica statusów) czekają poza repozytorium i wracają, gdy obejmie je instrukcja etapu.

Stosujemy **tylko cztery wzorce projektowe**: Fabryka (fabryka prosta z rejestrem typów), Decorator, Strategy i Observer. Nie wprowadzamy innych ani w kodzie, ani w dokumentacji.

## Spec-Driven Development

Każda nowa funkcja zaczyna się od specyfikacji w [`specs/czarna-tawerna/`](specs/czarna-tawerna/):

1. [`requirements.md`](specs/czarna-tawerna/requirements.md) - dopisz lub zmień wymaganie (W0-W9 funkcjonalne, N1-N11 niefunkcjonalne); kryteria w notacji EARS po polsku, z etykietą typu, np. `[Ubiquitous]` System POWINIEN…, `[Event-driven]` GDY…, `[Unwanted]` JEŚLI…, TO…,
2. [`design.md`](specs/czarna-tawerna/design.md) - opisz, jak to zaprojektować (diagramy w Mermaid),
3. [`tasks.md`](specs/czarna-tawerna/tasks.md) - dodaj zadanie z osobą i numerami wymagań,
4. dopiero potem kod i testy; po wykonaniu zadania odhacz je w `tasks.md`.

## Konwencje kodu

- Nazwy klas, metod i funkcji **po angielsku** (wymóg etapu 2, PEP 8), np. `Cart`, `MenuItemFactory`, `load_menu`.
- Wszystko inne **po polsku**: nazwy pakietów i plików, atrybuty, parametry, zmienne, stałe, klucze JSON, nazwy testów i fixture'ów, komentarze, docstringi, teksty interfejsu. Identyfikatory bez polskich znaków (`pozycje`, `cena_bazowa`), komentarze i teksty - z polskimi znakami.
- Styl PEP 8 sprawdzany przez `pycodestyle` (`setup.cfg`): linie do 99 znaków, komentarze i docstringi do 72.
- Logika w pakiecie `czarna_tawerna` **nie importuje Streamlita**; `app.py` to wyłącznie prezentacja i rozmawia z logiką przez klasę `Tavern`.
- Zależności między pakietami idą w jedną stronę: `interfejs` → `zamowienia` → `menu` → `pieniadze`.
- Kwoty w groszach (`int`); w JSON ceny w złotych, zamieniane funkcją `pln()`, wyświetlane przez `format_pln()`.
- Błędy logiki: `ValueError` (niedozwolona operacja) lub `KeyError` (brak id).

## Testy

- Testy są w `tests/`, po jednym pliku na pakiet; testujemy logikę, nie interfejs Streamlit.
- Każdy test sprawdza konkretny wynik, a nie tylko to, że kod nie zgłasza błędu; przypadki błędne też testujemy.
- Fixture'y `menu` i `tawerna` (`tests/conftest.py`) korzystają z prawdziwego `dane/menu.json` - po zmianie menu sprawdź testy.

Przed wysłaniem zmian:

```bash
pytest
pycodestyle czarna_tawerna app.py tests
```

## Praca z repozytorium

1. Przed rozpoczęciem pracy pobierz zmiany: `git pull`.
2. Większą zmianę rób na osobnej gałęzi (`git switch -c nazwa-zmiany`) i zgłoś przez pull request - szablon PR zawiera listę kontrolną. Drobne poprawki (literówki, dokumentacja) można wysłać prosto na `main`.
3. Commity: krótki opis po polsku, co i po co zmieniono, np. „Koszyk: usuwanie pozycji po tożsamości wpisu”.
4. Jeśli push zostanie odrzucony, bo ktoś wysłał zmiany wcześniej: `git pull --rebase`, a potem ponownie `git push`.
5. Do repozytorium **nie trafiają**: `.venv/`, pliki tymczasowe, gotowe pliki sprawozdania (DOCX/PDF), instrukcje prowadzącego i oddane PDF-y z numerami albumów (zob. `.gitignore`).

## Zgłoszenia (Issues)

Błędy i zadania zgłaszamy w zakładce **Issues** - są gotowe szablony „Błąd” i „Zadanie”. Problemy z bezpieczeństwem zgłaszamy zgodnie z [`SECURITY.md`](SECURITY.md), a zasady komunikacji opisuje [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Sprawozdanie

Sprawozdanie powstaje z generatora `sprawozdanie/generuj_sprawozdanie.py` (wymaga `python-docx`). Zmiany treści wprowadzamy w generatorze, a ręczne poprawki w Wordzie trzeba też przenieść do generatora - inaczej znikną przy następnym `--nadpisz`. Wytyczne redakcyjne: Times New Roman 12, marginesy 2 cm, tekst wyjustowany, łącznik „ - ” zamiast pauzy „—”, tabele jak w etapie 1 (zwykła siatka bez kolorów).
