# Zadania - Czarna Tawerna

Trzecia część specyfikacji: [wymagania](requirements.md) → [projekt](design.md) → **zadania** (ten plik).

Oznaczenia: `[x]` zrobione, `[ ]` do zrobienia. Przy zadaniu - osoba odpowiedzialna i wymagania, które realizuje.

Kolejność prac: najpierw Menu → równolegle Personalizacja i Zamówienia → Interfejs (od początku może pracować na danych testowych).

## Etap 1 - koncepcja (termin 6.11.2026, 23:59)

- [x] 1.1 Strona tytułowa i rozdział 1 sprawozdania (zespół, technologia, koncepcja lokalu, wstępne menu) - Krystian Rutkowski
- [x] 1.2 Generator sprawozdania `sprawozdanie/generuj_sprawozdanie.py`
- [x] 1.3 Zgoda prowadzącego na zespół 4-osobowy
- [x] 1.4 Ręczne poprawki w Wordzie i eksport do PDF (`sprawozdanie/etap1_pdf/`)
- [ ] 1.5 Każda osoba wgrywa własny plik `E1_Nazwisko_Imie_nralbumu.pdf`

## Szkielet aplikacji (wersja wstępna)

### Wspólne

- [x] 2.1 Środowisko `.venv`, `requirements.txt`, `pyproject.toml` (konfiguracja pytest) - _N1_
- [x] 2.2 Moduł `pieniadze.py`: kwoty w groszach, `pln()` i `format_pln()` - _N5, W9.3_

### Rola 1 - Menu (Wiktor Purgał)

- [x] 3.1 Klasy `MenuItem` (abstrakcyjna), `Drink`, `Dish`, `Size`, `AddOn`, `Category`, `Menu` - _W1.2, W1.3, W2.1, W2.2_ (`Size`, `AddOn` → poczekalnia)
- [x] 3.2 Dane menu w `dane/menu.json` (5 kategorii, 25 pozycji, 12 dodatków) - _W1.2_ (rozmiary i dodatki → poczekalnia)
- [x] 3.3 `MenuItemFactory` z rejestracją typów (fabryka prosta z rejestrem) - _W1.4, W1.5_
- [x] 3.4 `load_menu()` - _W1.1_
- [x] 3.5 Testy `tests/test_menu.py`

### Rola 2 - Personalizacja (Dariusz Lorenz) → poczekalnia

- [x] 4.1 `Product`, `BaseProduct`, dekorator `AddOnDecorator` (Decorator) - _W3.2, W3.3, W3.5_
- [x] 4.2 Domyślny rozmiar i walidacja rozmiaru - _W2.3, W2.4_
- [x] 4.3 Odrzucanie niepasujących dodatków - _W3.1, W3.4_
- [x] 4.4 Testy `tests/test_personalizacja.py`

### Rola 3 - Zamówienia (Katarzyna Pater)

- [x] 5.1 `Cart` i `CartItem` - _W4_
- [x] 5.2 `DiscountStrategy`, `NoDiscount`, `PercentageDiscount` (Strategy) - _W5.1, W5.3, W5.4_ → poczekalnia
- [x] 5.3 `Order` ze statusami i przejściami - _W6_ → poczekalnia
- [x] 5.4 Powiadamianie obserwatorów o zmianie statusu (Observer - podmiot) - _W7.3_ → poczekalnia
- [x] 5.5 Testy `tests/test_zamowienia.py`

### Rola 4 - Interfejs i integracja (Krystian Rutkowski)

- [x] 6.1 Klasa `Tavern` - stan sesji kiosku - _N2_
- [x] 6.2 `StatusBoard` (Observer - obserwator) - _W7.1, W7.2_ → poczekalnia
- [x] 6.3 `app.py`: menu w zakładkach, koszyk w panelu bocznym, promocje, zamówienia, tablica - _W0.1, W5.2, W9.1-9.3_ (promocje, zamówienia, tablica → poczekalnia)
- [x] 6.4 Testy `tests/test_tawerna.py`
- [x] 6.4a Wyraźny komunikat z numerem zamówienia po kliknięciu „Zamawiam” - _W0.3_ → poczekalnia
- [x] 6.4b Wydzielić i nazwać sekcję „Panel obsługi” (przyciski „Dalej ▶” i „Anuluj”), oddzieloną od części dla klienta - _W9.4_ → poczekalnia
- [ ] 6.5 Paragon PDF (fpdf2) z czcionką TTF obsługującą polskie znaki - _W8_
- [ ] 6.6 Przycisk pobierania paragonu w `app.py` - _W8.1_
- [ ] 6.7 Testy paragonu (np. czy PDF powstaje i zawiera numer zamówienia)

## Etap 2 - menu i koszyk (termin: do uzupełnienia)

Instrukcja: `req/etap2.md`. Funkcje etapu (menu, koszyk, fabryka, oddzielenie logiki) już działają - zostają nazwy po angielsku, brakujące testy, README i rozdział 2 sprawozdania.

### Decyzje zespołu

- [x] 8.1 Zakres angielskich nazw - decyzja (2026-11-02): tylko klasy, metody i funkcje; reszta po polsku - cały zespół - _N10_
- [x] 8.2 Nazwa wariantu fabryki - decyzja (2026-11-02): „Fabryka (fabryka prosta z rejestrem typów)”; poprawione N3, `design.md`, README, CLAUDE.md, rozdział 1 (tabela zespołu) i generator - Wiktor Purgał, cały zespół - _W1.5, N3_

### Kod

- [x] 8.3 Nazwy po angielsku w pakiecie `menu` (+ testy `test_menu.py`) - Wiktor Purgał - _N10_
- [x] 8.4 Nazwy po angielsku w pakiecie `personalizacja` (+ testy) - Dariusz Lorenz - _N10_
- [x] 8.5 Nazwy po angielsku w pakiecie `zamowienia` (+ testy) - Katarzyna Pater - _N10_
- [x] 8.6 Nazwy po angielsku w `interfejs`, `pieniadze.py`, `app.py`, `conftest.py`; integracja całości - Krystian Rutkowski - _N10_
- [x] 8.7 Sprawdzenie stylu PEP 8 (`pycodestyle`, konfiguracja w `setup.cfg`: linie do 99 znaków, docstringi i komentarze do 72) - pakiet, `app.py` i testy bez uwag - Krystian Rutkowski - _N10_
- [x] 8.8 Test usuwania pozycji z koszyka i usuwania pozycji spoza koszyka (błąd z czytelnym komunikatem; `Cart.remove` zgłasza teraz „Tej pozycji nie ma w koszyku”) - Katarzyna Pater - _W4.3, W4.5, N6_
- [x] 8.9 Test dokładności kwot, np. 1,10 zł + 2,20 zł = 3,30 zł - Katarzyna Pater - _W4.6, N5_
- [x] 8.10 Test rejestracji nowego typu pozycji w fabryce (`register`) oraz test, że nowa kategoria i danie wymagają tylko zmiany pliku menu (W1.7); test właściwego typu już był - Wiktor Purgał - _W1.5, W1.6, N6_
- [x] 8.11 Wszystkie testy przechodzą po zmianie nazw - cały zespół - _N6_
- [x] 8.11a Ograniczenie kodu do zakresu etapu 2 (decyzja 2026-11-02): rozmiary, dodatki i Decorator, promocje (Strategy), zamówienie ze statusami, tablica statusów (Observer) i panel obsługi przeniesione do `../Projekt_poczekalnia/` (opis w `POCZEKALNIA.md`); w projekcie: `MenuItem` z ceną i abstrakcyjnym `kind()`, `Cart`/`CartItem` z pozycją menu, `Tavern.add_to_cart()`, `app.py` z menu i koszykiem; 22 testy, PEP 8 bez uwag - Krystian Rutkowski - _W1, W4, W9.1-9.3, N6_
- [x] 8.11b Menu w kafelkach zamiast rozwijanych belek, zdjęcia poglądowe pozycji z Wikimedia Commons (wolne licencje, `dane/zdjecia/ZRODLA.md`) i grafika zastępcza; dostosowany skrypt zrzutu kiosku - Krystian Rutkowski - _W9.1, W9.5, W9.6_
- [x] 8.11c Grafiki produktów wygenerowane w Nano Banana (Google Gemini) zamiast zdjęć z Wikimedia Commons; `ZRODLA.md`, nowy zrzut kiosku, informacja o pochodzeniu grafik w punkcie 2.5 sprawozdania - Krystian Rutkowski - _W9.5_

### Dokumentacja

- [x] 8.12 Aktualizacja `design.md`, `README.md` i `CLAUDE.md` po zmianie nazw (diagramy, nazwy klas, status etapu) - Krystian Rutkowski - _N9, N10_
- [x] 8.12a README: instrukcja instalacji, konfiguracji i uruchomienia dla Windows, Linuksa i macOS; `requirements.txt`: `streamlit>=1.65` (starsze wersje nie mają `alt` w `st.image`); sprawdzone na Pythonie 3.10, 3.11 i 3.14 (Windows) - Krystian Rutkowski - _N1, N9_
- [x] 8.12b Ograniczenie testów do 12 (4 przypadki błędne) - zostają testy fabryki, koszyka i `Tavern` wymagane instrukcją etapu 2; usunięte zdublowane i drobne; odświeżony `zrzut_pytest.png` i tekst punktu 2.5 - Krystian Rutkowski - _N6_
- [x] 8.12c Zakładka „O twórcach” w kiosku: opis projektu i karty zespołu (imię i nazwisko, piracka rola, obszar), bez numerów albumów - Krystian Rutkowski - _W9.7_
- [ ] 8.13 Poprawki w rozdziale 1 wg uwag prowadzącego do etapu 1 - Krystian Rutkowski - _N11_

### Sprawozdanie - rozdział 2 „Menu i koszyk”

- [ ] 8.14 2.1 Diagram klas UML logiki (Mermaid → PNG) - Dariusz Lorenz; obrazek gotowy: `sprawozdanie/zasoby/diagram_klas_etap2.png` (z `design.md`); opis - wersja robocza w generatorze (2026-11-02), do przeglądu
- [ ] 8.15 2.2 Fabryka w projekcie: wariant, role klas, dodawanie dania lub kategorii - Wiktor Purgał - wersja robocza w generatorze (2026-11-02), do przeglądu
- [ ] 8.16 2.3 Oddzielenie logiki od interfejsu - Krystian Rutkowski - wersja robocza w generatorze (2026-11-02), do przeglądu
- [ ] 8.17 2.4 Decyzje projektowe z rozważanymi alternatywami (kwoty, menu w JSON, pakiety, koszyk) - Katarzyna Pater - wersja robocza w generatorze (2026-11-02), do przeglądu
- [x] 8.18 2.5 Zrzuty ekranu: kiosk z menu i koszykiem (`zrzut_kiosk_menu_koszyk.png`, Edge sterowany przez Playwright), wynik `pytest -v` (`zrzut_pytest.png`, obraz prawdziwego wyjścia polecenia) - w `sprawozdanie/zasoby/`, skrypty w `sprawozdanie/narzedzia/` - Krystian Rutkowski
- [ ] 8.19 Rozdział 2 w generatorze `sprawozdanie/generuj_sprawozdanie.py` i eksport do `sprawozdanie.pdf` - Krystian Rutkowski - _N11_ (rozdział 2 jest w generatorze; `--robocza` zapisuje `programowanie2_sprawozdanie_robocza.docx`; zostaje przegląd, scalenie z DOCX z ręcznymi poprawkami i eksport)

### Oddanie

- [ ] 8.20 Archiwa `E2_Nazwisko_Imie_nralbumu.zip` (kod, testy, `README.md`, `requirements.txt`, `sprawozdanie.pdf`) bez `.venv/`, `__pycache__/`, `.pytest_cache/`; generator sprawozdania i DOCX nie wchodzą do archiwum (narzędzie, nie kod aplikacji) - Krystian Rutkowski - _N7_
- [ ] 8.21 Każda osoba wgrywa własne archiwum na platformę - cały zespół

## Do ustalenia po instrukcjach kolejnych etapów

- [x] 7.1 Uzupełnić wymagania i zadania o etap 2
- [ ] 7.2 Uzupełnić wymagania i zadania o etap 3
- [ ] 7.3 Uzupełnić wymagania i zadania o etap 4
- [ ] 7.4 Decyzja: program lojalnościowy (Karta Załogi) i zestawy
- [ ] 7.4a Decyzja: osobny widok obsługi zamiast sekcji w widoku kiosku
- [ ] 7.5 Rozdziały sprawozdania - każda osoba opisuje swoją część i swój wzorzec
- [ ] 7.6 Archiwum ZIP do oddania bez `.venv/`, `__pycache__/`, `.pytest_cache/` - _N7_
- [ ] 7.7 Przygotowanie do obrony - każda osoba zna cały kod - _N8_
