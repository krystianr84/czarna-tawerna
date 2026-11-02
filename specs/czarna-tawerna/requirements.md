# Wymagania - Czarna Tawerna

Specyfikacja prowadzona metodą Spec-Driven Development: **wymagania** (ten plik) → [projekt](design.md) → [zadania](tasks.md).

Status: ustalenia z etapów 1 i 2. Instrukcje etapów 3-4 nie zostały jeszcze opublikowane, więc wymagania będą uzupełniane. Przypisanie wymagań do etapów - w sekcji „Wymagania etapów”.

**Stan kodu (2026-11-02):** projekt zawiera tylko zakres etapu 2 (W1, W4, W9.1-9.3). Wymagania oznaczone „(poczekalnia)” są zaprojektowane i zaimplementowane w `../Projekt_poczekalnia/` (opis w `POCZEKALNIA.md`) i wrócą do projektu w etapie, którego instrukcja je obejmie.

## Notacja EARS

Kryteria akceptacji zapisano w notacji EARS (Easy Approach to Requirements Syntax). Każde kryterium ma etykietę typu:

| Etykieta | Kiedy obowiązuje | Szablon |
|---|---|---|
| `[Ubiquitous]` | zawsze | System POWINIEN … |
| `[Event-driven]` | po zdarzeniu | GDY …, system POWINIEN … |
| `[State-driven]` | dopóki trwa stan | PODCZAS …, system POWINIEN … |
| `[Unwanted]` | przy błędzie lub niepożądanej sytuacji | JEŚLI …, TO system POWINIEN … |
| `[Optional]` | tylko dla wybranych elementów | DLA …, system POWINIEN … |

## Wprowadzenie

Czarna Tawerna to tawerna-kawiarnia w klimacie pirackim. System działa jak kiosk samoobsługowy: klient przegląda menu, komponuje produkty (rozmiar „statku” i dodatki - „łupy”), wybiera promocję, składa zamówienie i śledzi jego status na tablicy.

Źródła wymagań: instrukcje etapów 1 i 2 (`req/etap1.md`, `req/etap2.md`), wprowadzenie prowadzącego (`req/wprowadzenie.md`) i ustalenia zespołu (`dane_projektu.md`).

## Słownik

| Pojęcie | Znaczenie |
|---|---|
| Klient | osoba, która samodzielnie składa zamówienie w kiosku |
| Obsługa | pracownik tawerny (kasa, kuchnia), który zmienia status zamówienia |
| Kiosk | samoobsługowe stanowisko zamówień, jak w McDonald's czy KFC |
| Panel obsługi | część interfejsu do zmiany statusu zamówień; na razie w tym samym widoku co kiosk (uproszczenie, W9.4) |
| Pozycja menu | napój lub danie z karty, z ceną bazową |
| Rozmiar | rozmiar napoju: Szalupa 250 ml, Bryg 350 ml (+3 zł), Galeon 450 ml (+5 zł) |
| Łup (dodatek) | płatny dodatek do pozycji, np. mleko roślinne, bita śmietana |
| Produkt | pozycja menu z wybranym rozmiarem i dodatkami |
| Koszyk | produkty wybrane przed złożeniem zamówienia |
| Promocja | sposób liczenia rabatu od sumy zamówienia |
| Tablica statusów | ekran pokazujący zmiany statusu zamówień |

## Wymagania funkcjonalne

### W0. Kiosk samoobsługowy (etap 2: menu → koszyk; reszta ścieżki - poczekalnia)

**Historyjka:** Jako klient chcę sam złożyć zamówienie w kiosku, bez pomocy obsługi, tak jak w McDonald's czy KFC.

1. `[Ubiquitous]` System POWINIEN umożliwiać klientowi samodzielne przejście całej ścieżki zamówienia: przegląd menu → wybór rozmiaru i dodatków → koszyk → promocja → złożenie zamówienia.
2. `[Ubiquitous]` System POWINIEN prowadzić klienta tak, żeby nie potrzebował pomocy obsługi ani instrukcji.
3. `[Event-driven]` GDY klient złoży zamówienie, system POWINIEN pokazać mu numer zamówienia, po którym rozpozna je na tablicy statusów.

### W1. Menu (rola 1 - Nawigator)

**Historyjka:** Jako klient chcę przeglądać menu podzielone na kategorie, żeby szybko znaleźć to, na co mam ochotę.

1. `[Event-driven]` GDY aplikacja startuje, system POWINIEN wczytać menu z pliku `dane/menu.json`.
2. `[Ubiquitous]` System POWINIEN pokazywać menu podzielone na kategorie (co najmniej 3 kategorie i 5 pozycji); obecnie 5 kategorii i 25 pozycji.
3. `[Ubiquitous]` System POWINIEN pokazywać przy każdej pozycji nazwę, krótki opis, cenę bazową i oznaczenia (np. „wege”, „ostre”).
4. `[Unwanted]` JEŚLI plik menu zawiera pozycję nieznanego typu, TO system POWINIEN zgłosić błąd z nazwą tego typu.
5. `[Ubiquitous]` System POWINIEN pozwalać dodać nowy rodzaj pozycji bez zmiany istniejącego kodu tworzącego pozycje.
6. `[Ubiquitous]` System POWINIEN tworzyć pozycje menu wyłącznie przez fabrykę; kod interfejsu NIE POWINIEN wywoływać konstruktorów pozycji (etap 2).
7. `[Ubiquitous]` System POWINIEN pozwalać dodać nową pozycję lub kategorię przez samą zmianę pliku `dane/menu.json`, bez zmiany kodu.

### W2. Rozmiary napojów (rola 2 - Kuk) (poczekalnia)

**Historyjka:** Jako klient chcę wybrać rozmiar napoju, żeby zamówić tyle, ile wypiję.

1. `[Ubiquitous]` System POWINIEN oferować napoje w rozmiarach Szalupa, Bryg i Galeon, z dopłatą zależną od rozmiaru.
2. `[Optional]` DLA pozycji z ograniczoną listą rozmiarów (Espresso Kapitana: tylko Szalupa i Bryg) system POWINIEN oferować tylko rozmiary z tej listy.
3. `[Unwanted]` JEŚLI klient nie wybierze rozmiaru napoju, TO system POWINIEN przyjąć najmniejszy dostępny rozmiar.
4. `[Unwanted]` JEŚLI dla dania (prowiant, desery) podano rozmiar, TO system POWINIEN odrzucić taki wybór.

### W3. Dodatki - łupy (rola 2 - Kuk) (poczekalnia)

**Historyjka:** Jako klient chcę dobrać dodatki do produktu, żeby dopasować go do swojego gustu.

1. `[Ubiquitous]` System POWINIEN pokazywać przy pozycji tylko te dodatki, które do niej pasują (wg kategorii lub konkretnej pozycji).
2. `[Event-driven]` GDY klient doda dodatek, system POWINIEN doliczyć jego cenę do ceny produktu.
3. `[Ubiquitous]` System POWINIEN pozwalać dodać do produktu dowolną liczbę dodatków.
4. `[Unwanted]` JEŚLI dodatek nie pasuje do pozycji, TO system POWINIEN go odrzucić.
5. `[Ubiquitous]` System POWINIEN opisywać produkt nazwą, rozmiarem i listą dodatków, np. „Latte Bosmana (Bryg) + Syrop smakowy”.

### W4. Koszyk (rola 3 - Kwatermistrz)

**Historyjka:** Jako klient chcę zebrać kilka produktów w koszyku, żeby zamówić je razem.

1. `[Event-driven]` GDY klient doda produkt z ilością, system POWINIEN umieścić go w koszyku.
2. `[Unwanted]` JEŚLI ilość jest mniejsza niż 1, TO system POWINIEN odrzucić pozycję.
3. `[Ubiquitous]` System POWINIEN pozwalać usunąć pozycję z koszyka.
4. `[Ubiquitous]` System POWINIEN pokazywać wartość każdej pozycji i sumę koszyka.
5. `[Unwanted]` JEŚLI usuwana pozycja nie należy do koszyka, TO system POWINIEN zgłosić błąd i nie zmieniać koszyka.
6. `[Ubiquitous]` System POWINIEN liczyć wartość pozycji i sumę koszyka dokładnie, bez błędów zaokrągleń (N5), np. 1,10 zł + 2,20 zł = 3,30 zł.

### W5. Promocje (rola 3 - Kwatermistrz) (poczekalnia)

**Historyjka:** Jako klient chcę skorzystać z promocji, żeby zapłacić mniej.

1. `[Ubiquitous]` System POWINIEN pozwalać wybrać jedną promocję do zamówienia: brak promocji, Happy hour (-10%), Dzień pirata (-20%).
2. `[Event-driven]` GDY klient wybierze promocję, system POWINIEN pokazać sumę, rabat i kwotę do zapłaty.
3. `[Unwanted]` JEŚLI procent rabatu jest spoza przedziału 1-100, TO system POWINIEN odrzucić taką promocję.
4. `[Ubiquitous]` System POWINIEN pozwalać dodać nowy rodzaj promocji bez zmiany kodu zamówienia.

### W6. Zamówienie i jego cykl życia (rola 3 - Kwatermistrz) (poczekalnia)

**Historyjka:** Jako klient chcę złożyć zamówienie i wiedzieć, na jakim jest etapie.

1. `[Event-driven]` GDY klient złoży zamówienie, system POWINIEN nadać mu kolejny numer, ustawić status „Nowe” i opróżnić koszyk.
2. `[Unwanted]` JEŚLI koszyk jest pusty, TO system POWINIEN uniemożliwić złożenie zamówienia.
3. `[Ubiquitous]` System POWINIEN pozwalać obsłudze prowadzić zamówienie kolejno przez statusy: Nowe → Opłacone → W przygotowaniu → Gotowe do odbioru → Wydane.
4. `[State-driven]` PODCZAS gdy zamówienie ma status Nowe lub Opłacone, system POWINIEN pozwalać obsłudze je anulować.
5. `[Unwanted]` JEŚLI ktoś próbuje zmienić status zamówienia zakończonego (Wydane, Anulowane), TO system POWINIEN odrzucić tę zmianę.
6. `[Ubiquitous]` System NIE POWINIEN zmieniać złożonego zamówienia, gdy później zmienia się koszyk.

### W7. Tablica statusów (rola 4 - Szyper) (poczekalnia)

**Historyjka:** Jako klient chcę widzieć na tablicy, że moje zamówienie jest gotowe, jak na ekranie w fast foodzie.

1. `[Event-driven]` GDY status zamówienia się zmieni, system POWINIEN automatycznie dopisać zdarzenie na tablicy (numer, poprzedni i nowy status).
2. `[Ubiquitous]` System POWINIEN pokazywać ostatnie zdarzenia, od najnowszego.
3. `[Ubiquitous]` System POWINIEN pozwalać podpiąć do zamówienia dowolnych obserwatorów, tak żeby zamówienie nie zależało od konkretnej klasy tablicy.

### W8. Paragon PDF (rola 4 - Szyper) - planowane (poczekalnia)

**Historyjka:** Jako klient chcę dostać paragon, żeby mieć potwierdzenie zamówienia.

1. `[Event-driven]` GDY zamówienie zostanie złożone, system POWINIEN pozwolić pobrać paragon w formacie PDF.
2. `[Ubiquitous]` System POWINIEN umieszczać na paragonie numer zamówienia, produkty z rozmiarami i dodatkami, ilości, ceny, sumę, rabat z opisem promocji i kwotę do zapłaty.
3. `[Ubiquitous]` System POWINIEN poprawnie wyświetlać polskie znaki na paragonie.

### W9. Interfejs kiosku (rola 4 - Szyper) (etap 2: W9.1-9.3 w zakresie menu i koszyka, W9.5-9.7; W9.4 - poczekalnia)

**Historyjka:** Jako klient chcę obsługiwać kiosk w przeglądarce bez instrukcji.

1. `[Ubiquitous]` System POWINIEN mieć interfejs graficzny w Streamlit: menu w zakładkach kategorii, koszyk w panelu bocznym, lista zamówień i tablica statusów.
2. `[State-driven]` PODCZAS jednej sesji przeglądarki system POWINIEN zachowywać koszyk i zamówienia między przeładowaniami strony.
3. `[Ubiquitous]` System POWINIEN pokazywać kwoty w formacie „14,50 zł”.
4. `[Ubiquitous]` System POWINIEN udostępniać panel obsługi do zmiany statusu i anulowania zamówień. Na razie panel jest w tym samym widoku co kiosk, w osobnej sekcji (instrukcja etapu 2 tego nie rozstrzyga; decyzja zespołu - zadanie 7.4a).
5. `[Ubiquitous]` System POWINIEN pokazywać menu jako kafelki z grafiką poglądową pozycji; grafika to plik `dane/zdjecia/<id>.jpg`, a jej pochodzenie (generowanie AI) jest opisane w `dane/zdjecia/ZRODLA.md` i w sprawozdaniu (etap 2).
6. `[Unwanted]` JEŚLI dla pozycji nie ma pliku zdjęcia, TO system POWINIEN pokazać grafikę zastępczą `dane/zdjecia/brak.jpg` (dodanie pozycji nadal wymaga tylko zmiany `dane/menu.json`, W1.7).
7. `[Ubiquitous]` System POWINIEN mieć zakładkę „O twórcach” (ostatnią, za kategoriami menu) z krótkim opisem projektu i kartami członków zespołu: imię i nazwisko, piracka rola, obszar w projekcie, a na dole obrazek załogi `dane/zdjecia/crew.png`; bez numerów albumów, bo kiosk widzą klienci (etap 2).

## Wymagania niefunkcjonalne

| Nr | Wymaganie |
|---|---|
| N1 | Python 3.10+, Streamlit, pytest, fpdf2 - technologia zadeklarowana w etapie 1, bez zmian w kolejnych etapach. |
| N2 | Logika jest oddzielona od interfejsu: pakiet `czarna_tawerna` nie importuje Streamlita. |
| N3 | Stosujemy tylko wzorce Fabryka (fabryka prosta z rejestrem typów, ang. Simple Factory), Decorator, Strategy i Observer (decyzja zespołu; wariant fabryki ustalony 2026-11-02, zadanie 8.2). |
| N4 | Kod przestrzega zasad SOLID od początku; klasy abstrakcyjne przez `ABC` i `@abstractmethod`. W końcowej wersji zasady SOLID są wskazane w kodzie. |
| N5 | Kwoty są liczone w groszach (`int`), żeby uniknąć błędów zaokrągleń typu `float` (np. `1.10 + 2.20 = 3.3000000000000003`). |
| N6 | Każda część ma testy jednostkowe pytest; wszystkie testy przechodzą. Od etapu 2 co najmniej 6 testów logiki, m.in. tworzenia pozycji przez fabrykę i działania koszyka, w tym przypadków błędnych; każdy test sprawdza konkretny wynik, a nie tylko brak wyjątku. |
| N7 | Archiwum do oddania (od etapu 2) nie zawiera `.venv/`, `__pycache__/` ani plików tymczasowych. |
| N8 | Każda osoba z zespołu rozumie cały kod i potrafi go obronić. |
| N9 | `README.md` zawiera imiona, nazwiska i numery albumów całego zespołu oraz polecenia instalacji zależności, uruchomienia aplikacji i uruchomienia testów; zależności są w `requirements.txt` (etap 2). |
| N10 | Nazwy klas, metod i funkcji są po angielsku, a styl kodu zgodny z PEP 8 (etap 2). Decyzja zespołu (2026-11-02): zmieniamy tylko te nazwy; pakiety, pliki, atrybuty, parametry, zmienne, stałe enumów, klucze JSON, nazwy testów, komentarze i teksty interfejsu zostają po polsku. PEP 8 sprawdza `pycodestyle` (konfiguracja w `setup.cfg`: linie do 99 znaków, komentarze i docstringi do 72 - limit dopuszczony przez PEP 8). Wymaganie dotyczy kodu aplikacji i testów; generator sprawozdania to narzędzie spoza archiwum do oddania. |
| N11 | Sprawozdanie rośnie z etapami: w każdym etapie dochodzi nowy rozdział, a poprzednie są poprawiane wg uwag prowadzącego; oddaje się je jako PDF. |

## Wymagania etapów

Co z wymagań musi działać i być opisane w danym etapie. Kod w projekcie odpowiada zakresowi bieżącego etapu; wymagania późniejszych etapów czekają w poczekalni (`../Projekt_poczekalnia/`).

| Etap | Zakres z instrukcji | Wymagania | Sprawozdanie | Oddanie |
|---|---|---|---|---|
| 1 | zespół, technologia, koncepcja lokalu, wstępne menu | N1, N11 | strona tytułowa, rozdział 1 | `E1_Nazwisko_Imie_nralbumu.pdf` |
| 2 | menu i koszyk, fabryka, logika oddzielona od interfejsu, testy, README | W1, W4, W9.1-9.3, N2, N4, N5, N6, N9, N10 | rozdział 2 „Menu i koszyk”: diagram klas UML, fabryka w projekcie, oddzielenie logiki od interfejsu, decyzje projektowe z rozważanymi alternatywami, zrzuty ekranu (aplikacja i wynik testów); poprawki w rozdziale 1 | `E2_Nazwisko_Imie_nralbumu.zip` z kodem, testami, `README.md`, `requirements.txt` i `sprawozdanie.pdf` (rozdziały 1-2), bez plików tymczasowych (N7) |
| 3-4 | po publikacji instrukcji | | | |

## Poza zakresem (na razie)

- Program lojalnościowy (Karta Załogi) i zestawy - odłożone do instrukcji kolejnych etapów.
- Osobny widok obsługi (np. druga strona Streamlit) - do decyzji, gdy panel obsługi wróci z poczekalni.
- Płatności, konta użytkowników i trwałe przechowywanie zamówień (np. baza danych).
