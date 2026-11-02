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

- Python 3.10+ (sprawdzone na 3.10, 3.11 i 3.14)
- [Streamlit](https://streamlit.io/) 1.65+ - interfejs graficzny (starsze wersje nie obsługują części użytych funkcji)
- pytest - testy jednostkowe
- fpdf2 - pliki PDF (paragon - planowany)

Wszystkie biblioteki są w `requirements.txt` i instalują się jednym poleceniem do środowiska wirtualnego `.venv` w folderze projektu - niczego nie instaluje się globalnie poza samym Pythonem i Gitem.

## Instalacja i uruchomienie

Instrukcja ma cztery kroki: (1) zainstaluj Pythona i Gita, (2) pobierz projekt, (3) utwórz środowisko i zainstaluj biblioteki, (4) uruchom aplikację. Kroki 1, 3 i 4 różnią się między systemami - wybierz swój. Wszystkie polecenia wpisuje się w terminalu (Windows: **PowerShell**, Linux i macOS: **Terminal**).

### 1. Python i Git

**Windows 10/11**

1. Zainstaluj Pythona 3.10 lub nowszego ze strony [python.org/downloads](https://www.python.org/downloads/). W pierwszym oknie instalatora **zaznacz „Add python.exe to PATH”**, potem „Install Now”. Zamiast tego można użyć polecenia `winget install Python.Python.3.12`.
2. Zainstaluj Gita ze strony [git-scm.com](https://git-scm.com/download/win) (domyślne opcje są w porządku) albo `winget install Git.Git`.
3. Zamknij i otwórz PowerShell na nowo, a potem sprawdź:

   ```powershell
   python --version   # Python 3.10 lub nowszy
   git --version
   ```

   Jeśli `python` otwiera Microsoft Store albo nie jest znany, użyj zamiast niego `py` (launcher Pythona) we wszystkich poleceniach poniżej albo zainstaluj Pythona jeszcze raz z zaznaczonym „Add to PATH”.

**Linux** (Ubuntu / Debian / Mint)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
python3 --version   # Python 3.10 lub nowszy
```

Fedora: `sudo dnf install python3 python3-pip git`, Arch: `sudo pacman -S python python-pip git`. Jeśli systemowy Python jest starszy niż 3.10, zainstaluj nowszy (np. Ubuntu 20.04: `sudo add-apt-repository ppa:deadsnakes/ppa` i `sudo apt install python3.12 python3.12-venv`, a potem używaj `python3.12` zamiast `python3`).

**macOS**

1. Zainstaluj [Homebrew](https://brew.sh) (polecenie ze strony głównej), a potem:

   ```bash
   brew install python git
   python3 --version   # Python 3.10 lub nowszy
   ```

2. Bez Homebrew: Pythona można pobrać z [python.org/downloads](https://www.python.org/downloads/macos/), a Gita zainstaluje system po pierwszym wpisaniu `git` w Terminalu (narzędzia Xcode Command Line Tools).

Na Linuksie i macOS polecenie nazywa się `python3`, a nie `python` (do czasu aktywacji `.venv`).

### 2. Pobranie projektu

Repozytorium jest prywatne - potrzebne jest konto GitHub z dostępem (zaproszenie do repozytorium). Najprościej przez Git (przy pierwszym pobraniu Git poprosi o zalogowanie do GitHuba w przeglądarce):

```bash
git clone https://github.com/krystianr84/czarna-tawerna.git
cd czarna-tawerna
```

Inne sposoby: `gh repo clone krystianr84/czarna-tawerna` (po `gh auth login` w [GitHub CLI](https://cli.github.com)) albo na stronie repozytorium **Code → Download ZIP** i rozpakowanie archiwum. Wszystkie dalsze polecenia wykonuje się w folderze projektu (tam, gdzie leży `app.py`).

### 3. Środowisko wirtualne i biblioteki

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jeśli aktywacja kończy się błędem „running scripts is disabled on this system”, zezwól raz na lokalne skrypty i powtórz aktywację:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

W wierszu poleceń `cmd.exe` aktywacja to `.venv\Scripts\activate.bat`.

**Linux i macOS (Terminal)**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Po aktywacji na początku wiersza terminala pojawia się `(.venv)`, a polecenia `python`, `pip`, `streamlit` i `pytest` korzystają z bibliotek projektu. Aktywację powtarza się w każdym nowym oknie terminala (krok 3 bez tworzenia `.venv` i instalacji), a kończy poleceniem `deactivate`.

Instalacja z `requirements.txt` wystarczy raz; po zmianie tego pliku (np. po `git pull`) trzeba ją powtórzyć.

### 4. Uruchomienie aplikacji

Przy aktywnym środowisku `.venv`, we wszystkich systemach:

```bash
streamlit run app.py
```

Streamlit sam otworzy przeglądarkę z kioskiem; jeśli tego nie zrobi, wejdź na **http://localhost:8501**. Aplikację zatrzymuje się w terminalu skrótem **Ctrl+C**.

Bez aktywacji środowiska:

- Windows: `.\uruchom.ps1` - skrypt korzysta z Pythona w `.venv` i działa z dowolnego folderu (dodatkowe argumenty przekazuje do Streamlita, np. `.\uruchom.ps1 --server.port 8502`),
- Linux i macOS: `.venv/bin/python -m streamlit run app.py`.

### Testy

```bash
pytest                              # wszystkie testy
pytest tests/test_zamowienia.py     # jeden plik
pytest -k test_suma_koszyka         # jeden test
```

Sprawdzenie stylu PEP 8 (narzędzie spoza `requirements.txt`, konfiguracja w `setup.cfg`):

```bash
pip install pycodestyle
pycodestyle czarna_tawerna app.py tests
```

### Konfiguracja

Aplikacja nie wymaga kluczy, haseł ani bazy danych - działa od razu po instalacji.

- `.streamlit/config.toml` - ustawienia kiosku: ukryty przycisk „Deploy” i menu dewelopera, wyłączone wysyłanie statystyk do Streamlita. Plik jest wczytywany, gdy aplikację uruchamia się z folderu projektu.
- `dane/menu.json` - menu (kategorie, pozycje, ceny w złotych); nowe danie lub kategorię dodaje się samą zmianą tego pliku, bez zmian w kodzie.
- `dane/zdjecia/<id>.jpg` - grafika pozycji o danym `id` z menu; pozycja bez grafiki dostaje `brak.jpg`.
- Inny port niż 8501: `streamlit run app.py --server.port 8502`.

### Najczęstsze problemy

| Problem | Rozwiązanie |
|---|---|
| `python` / `python3` nie jest rozpoznawany | Python nie jest w PATH - zainstaluj ponownie z „Add to PATH” (Windows) albo użyj `py` / `python3` |
| „running scripts is disabled” przy aktywacji (Windows) | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `error: externally-managed-environment` przy `pip install` (Linux, macOS) | biblioteki instaluje się tylko w aktywnym `.venv` - wykonaj najpierw `source .venv/bin/activate` |
| `No module named venv` / `ensurepip is not available` (Debian, Ubuntu) | `sudo apt install python3-venv` |
| `streamlit: command not found` | środowisko nie jest aktywne - aktywuj `.venv` (krok 3) albo użyj `python -m streamlit run app.py` |
| „Port 8501 is already in use” | aplikacja już działa w innym terminalu - zatrzymaj ją (Ctrl+C) albo użyj `--server.port 8502` |
| `TypeError: ... unexpected keyword argument` przy starcie | za stary Streamlit - `pip install -r requirements.txt --upgrade` (wymagany 1.65+) |
| Git przy `clone` zgłasza brak dostępu | repozytorium jest prywatne - zaakceptuj zaproszenie do repozytorium i zaloguj się do GitHuba |

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
sprawozdanie/           generator sprawozdania DOCX, narzędzia do zrzutów, zasoby (diagram, zrzuty)
.streamlit/config.toml  ustawienia Streamlit dla kiosku
uruchom.ps1             uruchomienie bez aktywacji .venv (Windows)
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

Sprawozdanie generuje skrypt `sprawozdanie/generuj_sprawozdanie.py` (plik wynikowy `sprawozdanie/programowanie2_sprawozdanie.docx`, nadpisywany tylko z opcją `--nadpisz`). Generator potrzebuje dodatkowo biblioteki `python-docx`, której celowo nie ma w `requirements.txt` (to narzędzie zespołu, nie część aplikacji):

```bash
pip install python-docx
python sprawozdanie/generuj_sprawozdanie.py --nadpisz
```

Gotowe pliki sprawozdania nie są przechowywane w repozytorium. Skrypty zrzutów ekranu opisuje `sprawozdanie/narzedzia/README.md`.

## Oddawanie

Od etapu 2 oddaje się archiwum ZIP z kodem i sprawozdaniem - **bez** `.venv/`, `__pycache__/` i `.pytest_cache/`.
