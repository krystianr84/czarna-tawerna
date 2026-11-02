"""Generuje sprawozdanie z projektu w formacie DOCX (do ręcznej edycji i eksportu do PDF).

Uruchomienie:  python sprawozdanie/generuj_sprawozdanie.py [--nadpisz | --robocza]

Bez --nadpisz skrypt nie nadpisze istniejącego pliku, żeby nie skasować ręcznych poprawek.
Z --robocza zapisuje wersję roboczą do osobnego pliku (zawsze nadpisywanego).
"""

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

ETAP = 2
KATALOG = Path(__file__).parent
WYJSCIE = KATALOG / "programowanie2_sprawozdanie.docx"
WYJSCIE_ROBOCZE = KATALOG / "programowanie2_sprawozdanie_robocza.docx"
ZASOBY = KATALOG / "zasoby"
LOGO = ZASOBY / "logo_ahe.png"
CZCIONKA_KODU = "Courier New"

CZCIONKA = "Times New Roman"
ROZMIAR_TEKSTU = Pt(12)
ROZMIAR_TABELI = Pt(10)
MARGINES = Cm(2)
SZEROKOSC_TEKSTU = 17.0  # cm: A4 (21 cm) minus marginesy

AKCENT = "1F1A17"   # tytuły
SZARY = RGBColor(0x55, 0x55, 0x55)

ZESPOL = [
    # (imię i nazwisko, piracka rola, nr albumu, rola, zakres prac, planowane wzorce)
    ("Krystian Rutkowski", "Szyper", "167040", "Interfejs i integracja",
     "interfejs Streamlit, paragon PDF, powiadomienia o zmianie statusu zamówienia, koordynacja sprawozdania",
     "Observer"),
    ("Katarzyna Pater", "Kwatermistrz", "167683", "Zamówienia",
     "koszyk, cykl życia zamówienia, promocje",
     "Strategy, Observer"),
    ("Dariusz Lorenz", "Kuk", "167014", "Personalizacja",
     "rozmiary napojów, dodatki, składanie produktu i wyliczanie ceny",
     "Decorator"),
    ("Wiktor Purgał", "Nawigator", "165328", "Menu",
     "model menu (klasy abstrakcyjne pozycji, kategorie), wczytywanie menu z pliku",
     "Fabryka"),
]
KIEROWNIK = ZESPOL[0][0]

# --- menu -----------------------------------------------------------------------
# (nazwa, krótki opis, oznaczenia, cena w zł); ceny napojów dla rozmiaru Szalupa
MENU = [
    ("Kawy z ładowni", [
        ("Espresso Kapitana", "mocne espresso", "", 9),
        ("Americano Rozbitka", "espresso z gorącą wodą", "", 11),
        ("Cappuccino Nawigatora", "espresso, mleczna pianka, kakao", "", 14),
        ("Latte Bosmana", "espresso z dużą ilością mleka", "", 15),
        ("Flat White Abordażu", "podwójne espresso z mlekiem", "", 15),
        ("Mokka Czarnej Bandery", "espresso, czekolada, mleko", "", 17),
        ("Latte Rajskiej Wyspy", "espresso z mlekiem kokosowym", "wege", 17),
    ]),
    ("Napoje z Tortugi", [
        ("Grog Bosmana", "korzenna herbata z pomarańczą", "", 14),
        ("Zielona Mgła", "matcha latte", "", 17),
        ("Złoty Dublon", "golden latte z kurkumą", "", 16),
        ("Czekolada Korsarza", "gorąca czekolada", "", 15),
        ("Herbata z Indii Wschodnich", "zielona herbata jaśminowa", "wege", 10),
    ]),
    ("Zimne trunki", [
        ("Cold Brew z Głębin", "kawa parzona na zimno", "wege", 16),
        ("Lemoniada Syreny", "niebieska lemoniada", "wege", 13),
        ("Frappe Krakena", "mrożona kawa z karmelem i chili", "ostre", 18),
        ("Poncz Karaibski", "ananas, mango, marakuja, limonka", "wege", 15),
    ]),
    ("Prowiant z kambuza", [
        ("Tost Kartografa", "tost z awokado i jajkiem", "", 19),
        ("Bajgiel Przemytnika", "bajgiel z łososiem i serkiem", "", 21),
        ("Wrap Bukaniera", "wrap z kurczakiem", "ostre", 23),
        ("Owsianka Majtka", "owsianka z mango i kokosem", "wege", 16),
        ("Rogalik Sternika", "maślany croissant", "", 11),
    ]),
    ("Skarby z kufra", [
        ("Skrzynia Skarbów", "brownie z orzechami", "", 14),
        ("Sernik Gubernatora", "sernik baskijski", "", 15),
        ("Cynamonowy Kompas", "bułka cynamonowa", "", 12),
        ("Banan Rozbitka", "karmelizowany banan", "wege", 13),
    ]),
]

# (nazwa, opis, dopłata)
ROZMIARY = [
    ("Szalupa", "250 ml", "-"),
    ("Bryg", "350 ml", "+3 zł"),
    ("Galeon", "450 ml", "+5 zł"),
]

# (nazwa, do czego, cena)
LUPY = [
    ("Mleko roślinne", "napoje mleczne", "+3 zł"),
    ("Mleko bez laktozy", "napoje mleczne", "+2 zł"),
    ("Dodatkowy shot espresso", "napoje kawowe", "+4 zł"),
    ("Syrop smakowy", "napoje", "+3 zł"),
    ("Bita śmietana", "napoje, desery", "+3 zł"),
    ("Pianki marshmallow", "czekolada, mokka", "+2 zł"),
    ("Posypka", "napoje", "+1 zł"),
    ("Złoty pył (jadalny brokat)", "napoje, desery", "+2 zł"),
    ("Kulka lodów", "desery, zimne trunki", "+5 zł"),
    ("Dodatkowe jajko", "Tost Kartografa", "+4 zł"),
    ("Podwójne awokado", "Tost Kartografa", "+5 zł"),
    ("Podwójny łosoś", "Bajgiel Przemytnika", "+7 zł"),
]


# --- pomocnicze -------------------------------------------------------------------

SIEROTKI = re.compile(r"(?<!\S)([aiouwzAIOUWZ]|za|na|do|od|po|we|ze) ")


def bez_sierotek(tekst):
    """Twarda spacja po krótkich słowach (i, w, z, za…), żeby nie zostawały na końcu wiersza."""
    return SIEROTKI.sub("\\1\u00a0", tekst)


def akapit(doc, tekst="", styl=None, size=None, italic=None):
    """Akapit z prostym formatowaniem: **pogrubienie** i `kod` (czcionka o stałej szerokości)."""
    p = doc.add_paragraph(style=styl)
    for i, kawalek in enumerate(bez_sierotek(tekst).split("**")):
        for j, czesc in enumerate(kawalek.split("`")):
            if not czesc:
                continue
            run = p.add_run(czesc)
            run.bold = i % 2 == 1
            run.italic = italic
            if j % 2 == 1:
                run.font.name = CZCIONKA_KODU
                run.font.size = Pt(11)
            elif size:
                run.font.size = size
    return p


def punkt(doc, tekst):
    """Punkt listy wypunktowanej."""
    return akapit(doc, tekst, styl="List Bullet")


def rysunek(doc, plik, szerokosc_cm, podpis):
    """Obrazek wyśrodkowany z podpisem pod spodem (podpis nie odrywa się od obrazka)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(str(ZASOBY / plik), width=Cm(szerokosc_cm))
    podp = akapit(doc, podpis, size=Pt(10), italic=True)
    podp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    podp.paragraph_format.space_after = Pt(10)
    return podp


def listing(doc, kod, podpis):
    """Fragment kodu: czcionka o stałej szerokości na jasnym tle, z podpisem."""
    podp = akapit(doc, podpis, size=Pt(10), italic=True)
    podp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    podp.paragraph_format.keep_with_next = True
    podp.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.left_indent = Cm(0.3)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F3F3F3")
    p._p.get_or_add_pPr().append(shd)
    for i, linia in enumerate(kod.strip("\n").split("\n")):
        if i:
            p.add_run().add_break()
        run = p.add_run(linia)
        run.font.name = CZCIONKA_KODU
        run.font.size = Pt(9.5)
    return p


WYROWNANIE = {"L": WD_ALIGN_PARAGRAPH.LEFT, "C": WD_ALIGN_PARAGRAPH.CENTER, "R": WD_ALIGN_PARAGRAPH.RIGHT}


def tabela(doc, wiersze, szerokosci, pogrubiona_kolumna=None, wyrownanie=None, wysrodkuj=False):
    """Zwykła tabela jak w etapie 1: siatka, pogrubiony nagłówek bez tła, bez cieniowania;
    „\\n” w tekście komórki zaczyna nowy akapit.

    wyrownanie - np. "CCCLL": wyrównanie kolumn w wierszach danych (nagłówek jest wtedy wyśrodkowany);
    wysrodkuj  - tabela wyśrodkowana na stronie, a tekst w komórkach wyśrodkowany w pionie.
    """
    t = doc.add_table(rows=len(wiersze), cols=len(wiersze[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER if wysrodkuj else WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    for c, szer in enumerate(szerokosci):
        t.columns[c].width = Cm(szer)
    for wiersz_tabeli in t.rows:
        # wiersz nie dzieli się między strony
        nie_dziel = OxmlElement("w:cantSplit")
        wiersz_tabeli._tr.get_or_add_trPr().append(nie_dziel)
    for r, wiersz in enumerate(wiersze):
        for c, tekst in enumerate(wiersz):
            kom = t.cell(r, c)
            kom.width = Cm(szerokosci[c])
            if wysrodkuj:
                kom.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if wyrownanie:
                wyr = WYROWNANIE["C" if r == 0 else wyrownanie[c]]
            else:
                wyr = WD_ALIGN_PARAGRAPH.LEFT
            for i, linia in enumerate(str(tekst).split("\n")):
                p = kom.paragraphs[0] if i == 0 else kom.add_paragraph()
                p.alignment = wyr
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                run = p.add_run(linia)
                run.font.size = ROZMIAR_TABELI
                run.bold = r == 0 or c == pogrubiona_kolumna
    # nagłówek powtarzany na kolejnych stronach
    trPr = t.rows[0]._tr.get_or_add_trPr()
    naglowek = OxmlElement("w:tblHeader")
    naglowek.set(qn("w:val"), "true")
    trPr.append(naglowek)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def numer_strony(akapit_):
    for typ, tekst in (("begin", None), (None, "PAGE"), ("end", None)):
        run = akapit_.add_run()
        if typ:
            fld = OxmlElement("w:fldChar")
            fld.set(qn("w:fldCharType"), typ)
            run._r.append(fld)
        else:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = tekst
            run._r.append(instr)


def przygotuj_dokument():
    doc = Document()
    # szablon python-docx ma <w:zoom> bez wymaganego atrybutu percent
    zoom = doc.settings.element.find(qn("w:zoom"))
    if zoom is not None:
        zoom.set(qn("w:percent"), "100")
    sekcja = doc.sections[0]
    sekcja.page_width, sekcja.page_height = Cm(21), Cm(29.7)
    for bok in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sekcja, bok, MARGINES)

    normal = doc.styles["Normal"]
    normal.font.name = CZCIONKA
    normal.font.size = ROZMIAR_TEKSTU
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), CZCIONKA)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    for nazwa, rozmiar, przed in (("Heading 1", 16, 0), ("Heading 2", 14, 12), ("Heading 3", 12, 8)):
        st = doc.styles[nazwa]
        st.font.name = CZCIONKA
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        st.font.size = Pt(rozmiar)
        st.font.bold = True
        st.font.color.rgb = RGBColor.from_string(AKCENT)
        st.paragraph_format.space_before = Pt(przed)
        st.paragraph_format.space_after = Pt(4)
        st.paragraph_format.keep_with_next = True
        for atr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            st.element.rPr.rFonts.attrib.pop(qn(atr), None)
    return doc


# --- treść ------------------------------------------------------------------------
def strona_tytulowa(doc):
    def srodek(tekst, rozmiar, odstep_przed=0, **kw):
        p = akapit(doc, tekst, size=Pt(rozmiar), **kw)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(odstep_przed)
        return p

    logo = doc.add_paragraph()
    logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo.paragraph_format.space_before = Pt(20)
    logo.add_run().add_picture(str(LOGO), width=Cm(14.9))
    srodek("Kierunek: Informatyka", 12)
    srodek("Programowanie obiektowe II - projekt semestralny", 12, odstep_przed=110)
    tytul = srodek("**Czarna Tawerna**", 28, odstep_przed=20)
    tytul.runs[0].font.color.rgb = RGBColor.from_string(AKCENT)
    srodek("System zamówień w pirackiej tawernie", 14)
    autorzy = srodek("**Autorzy**", 11, odstep_przed=110)
    autorzy.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for imie, _, album, *_ in ZESPOL:
        p = srodek(f"{imie} - nr albumu {album}", 11)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(2)
    srodek("Rok akademicki 2026/2027", 12, odstep_przed=90)

    # rozdział zaczyna się w nowej sekcji, żeby strona tytułowa nie miała stopki
    nowa = doc.add_section(WD_SECTION.NEW_PAGE)
    nowa.footer.is_linked_to_previous = False
    stopka = nowa.footer.paragraphs[0]
    stopka.alignment = WD_ALIGN_PARAGRAPH.LEFT
    tabulatory = stopka.paragraph_format.tab_stops
    # styl „Footer” z szablonu ma tabulatory pod marginesy 2,5 cm — usuwamy je
    for pozycja in (Twips(4680), Twips(9360)):
        tabulatory.add_tab_stop(pozycja, WD_TAB_ALIGNMENT.CLEAR)
    tabulatory.add_tab_stop(Cm(SZEROKOSC_TEKSTU), WD_TAB_ALIGNMENT.RIGHT)
    stopka.text = "Czarna Tawerna - sprawozdanie z projektu, PO II\t"
    numer_strony(stopka)
    for run in stopka.runs:
        run.font.size, run.font.color.rgb = Pt(9), SZARY


def rozdzial_1(doc):
    doc.add_heading("1. Koncepcja projektu", level=1)

    doc.add_heading("1.1. Zespół", level=2)
    akapit(doc, "Projekt realizuje czteroosobowy zespół. Kierownikiem projektu jest Krystian Rutkowski, "
                "który odpowiada za integrację części aplikacji i koordynację sprawozdania. Każda osoba "
                "odpowiada za wybrany obszar aplikacji, pisze do niego testy jednostkowe i opisuje go "
                "w sprawozdaniu; za całość projektu odpowiada cały zespół.")
    # kierownik ma rolę w tej samej linii, pozostali - w drugiej linii komórki
    osoby = [(f"{imie} ({piracka})" if imie == KIEROWNIK else f"{imie}\n({piracka})", *reszta)
             for imie, piracka, *reszta in ZESPOL]
    tabela(doc, [("Imię i nazwisko", "Nr albumu", "Rola", "Zakres prac", "Planowane wzorce")] + osoby,
           [3.4, 1.54, 2.5, 6.75, 2.81], wyrownanie="CCCCC", wysrodkuj=True)
    akapit(doc, "Podział jest wstępny i może zostać doprecyzowany w kolejnych etapach. Prace zaczynają się "
                "od modelu menu, na którym opierają się personalizacja i zamówienia; interfejs od początku "
                "powstaje równolegle na danych testowych. Logika aplikacji nie zależy od interfejsu.")

    doc.add_heading("1.2. Technologia", level=2)
    akapit(doc, "Projekt powstaje w zalecanej technologii: język **Python 3.10+**, interfejs graficzny "
                "**Streamlit**, testy jednostkowe **pytest**, generowanie plików PDF (paragonów) **fpdf2**. "
                "Klasy abstrakcyjne definiowane są za pomocą modułu **abc** (ABC, @abstractmethod).")

    doc.add_heading("1.3. Koncepcja lokalu", level=2)
    akapit(doc, "**Czarna Tawerna** to tawerna-kawiarnia w klimacie pirackich Karaibów z czasów złotej ery "
                "piractwa. Wnętrze przypomina portową tawernę z ciemnego drewna - latarnie, sieci i liny pod "
                "sufitem, mapy skarbów na ścianach, beczki zamiast stolików i szanty w tle. Napoje serwowane "
                "są w „rozmiarach statków” (Szalupa, Bryg, Galeon), a dodatki nazywane są „łupami”. W karcie "
                "są kawy z ziaren z Jamajki i Kolumbii, napoje bezkawowe (wszystkie bezalkoholowe), "
                "śniadania i przekąski z kuchnią karaibską w tle oraz desery.")
    akapit(doc, "Lokal jest skierowany do studentów, grup znajomych oraz miłośników przygody, filmów i gier "
                "o piratach - to miejsce spotkań „załóg” i wieczorów gier planszowych.")

    doc.add_heading("1.4. Wstępne menu", level=2)
    akapit(doc, "Menu obejmuje pięć kategorii i 25 pozycji, a także rozmiary napojów i dodatki. "
                "Ceny napojów podano dla rozmiaru Szalupa; większe rozmiary i dodatki zwiększają cenę. "
                "Espresso Kapitana występuje tylko w rozmiarach Szalupa i Bryg, a prowiant i desery nie mają "
                "rozmiarów. Oznaczenia: wege - pozycja wegańska, ostre - pozycja pikantna; wszystkie napoje "
                "są bezalkoholowe.")
    t = tabela_menu(doc)
    # jak w etapie 1: tabela menu zaczyna się w całości na nowej stronie
    t.rows[0].cells[0].paragraphs[0].paragraph_format.page_break_before = True


def tabela_menu(doc):
    """Menu jako zwykła tabela (jak w etapie 1); kategoria scalona w pionie i pogrubiona."""
    grupy = [(k, [(f"{n} ({u})" if u else n, o, f"{c} zł") for n, o, u, c in dania])
             for k, dania in MENU]
    grupy.append(("Rozmiary napojów", ROZMIARY))
    grupy.append(("Dodatki (łupy)", [(n, f"do: {d}", c) for n, d, c in LUPY]))

    szerokosci = (2.44, 6.5, 6.5, 1.56)
    wiersze = [("Kategoria", "Pozycja", "Opis", "Cena")]
    for kategoria, pozycje in grupy:
        wiersze += [(kategoria if i == 0 else "", *poz) for i, poz in enumerate(pozycje)]
    t = tabela(doc, wiersze, szerokosci, pogrubiona_kolumna=1)

    # scalenie komórek kategorii, ceny do prawej
    r = 1
    for kategoria, pozycje in grupy:
        for i in range(len(pozycje)):
            t.cell(r + i, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        scalona = t.cell(r, 0).merge(t.cell(r + len(pozycje) - 1, 0))
        for nadmiar in scalona.paragraphs[1:]:
            nadmiar._p.getparent().remove(nadmiar._p)
        scalona.paragraphs[0].runs[0].bold = True
        r += len(pozycje)
    return t


LISTING_FABRYKI = '''
class MenuItemFactory:
    def __init__(self) -> None:
        self._konstruktory: dict[str, ItemConstructor] = {
            "napoj": _create_drink,
            "danie": _create_dish,
        }

    def register(self, typ: str, konstruktor: ItemConstructor) -> None:
        self._konstruktory[typ] = konstruktor

    def create(self, dane: dict[str, Any], kategoria_id: str) -> MenuItem:
        typ = dane.get("typ")
        try:
            konstruktor = self._konstruktory[typ]
        except KeyError:
            raise ValueError(f"Nieznany typ pozycji: {typ!r}") from None
        return konstruktor(dane, kategoria_id)
'''

LISTING_NOWY_TYP = '''
@dataclass(frozen=True)
class ComboMeal(Dish):
    def kind(self) -> str:
        return "zestaw"

fabryka = MenuItemFactory()
fabryka.register("zestaw", utworz_zestaw)  # zwraca ComboMeal
menu = load_menu(PLIK_MENU, fabryka)
'''


def rozdzial_2(doc):
    tytul = doc.add_heading("2. Menu i koszyk", level=1)
    tytul.paragraph_format.page_break_before = True
    akapit(doc, "W etapie 2 powstała pierwsza działająca wersja aplikacji. Klient przegląda w kiosku menu "
                "podzielone na kategorie, dodaje pozycje do koszyka w wybranej ilości, usuwa je i widzi "
                "wartość koszyka. Kod obejmuje zakres tego etapu: rozmiary napojów, łupy, promocje "
                "i składanie zamówienia ze śledzeniem statusu zostaną dodane w kolejnych etapach. Zgodnie "
                "z konwencją Pythona (PEP 8) nazwy klas, metod i funkcji są po angielsku, a nazwy pól, "
                "zmiennych i modułów oraz komentarze - po polsku.")

    # --- 2.1 ---------------------------------------------------------------------
    doc.add_heading("2.1. Diagram klas", level=2)
    akapit(doc, "Rysunek 2.1 przedstawia klasy logiki aplikacji z pakietu `czarna_tawerna`. Centralną klasą "
                "menu jest abstrakcyjna klasa `MenuItem` (pozycja w karcie) z polami: identyfikator, nazwa, "
                "opis, cena, kategoria i oznaczenia (np. „wege”). Cena jest liczbą całkowitą w groszach. "
                "Klasa ma metodę `price()` oraz abstrakcyjną metodę `kind()`, którą nadpisują konkretne "
                "klasy `Drink` (napój) i `Dish` (danie). Dzięki temu nie da się utworzyć „pozycji w ogóle” - "
                "każda pozycja jest napojem albo daniem.")
    rysunek(doc, "diagram_klas_etap2.png", 10.5, "Rys. 2.1. Diagram klas logiki aplikacji (etap 2)")
    akapit(doc, "Klasa `Category` grupuje pozycje jednej kategorii (np. „Kawy z ładowni”), a `Menu` przechowuje "
                "listę kategorii i pozwala znaleźć pozycję po identyfikatorze (`item()`). Pozycje tworzy "
                "fabryka `MenuItemFactory` (punkt 2.2). Koszyk `Cart` składa się z wpisów `CartItem`; każdy "
                "wpis wskazuje pozycję menu i ilość, a jego wartość liczy metoda `value()`. Sumę koszyka "
                "zwraca `total()`. Klasa `Tavern` reprezentuje jedną sesję kiosku: łączy menu z koszykiem "
                "i udostępnia interfejsowi metodę `add_to_cart()`.")

    # --- 2.2 ---------------------------------------------------------------------
    doc.add_heading("2.2. Fabryka w projekcie", level=2)
    akapit(doc, "Menu jest zapisane w pliku `dane/menu.json`. Każda pozycja ma w nim pole `typ` o wartości "
                "„napoj” albo „danie”. Program musi na tej podstawie utworzyć obiekt właściwej klasy, a reszta "
                "kodu - wczytywanie menu, koszyk i interfejs - nie powinna znać konkretnych klas pozycji "
                "ani wywoływać ich konstruktorów. Tę odpowiedzialność przejmuje fabryka.")
    akapit(doc, "Wybraliśmy wariant **fabryki prostej z rejestrem typów** (ang. Simple Factory). Klasa "
                "`MenuItemFactory` przechowuje słownik, który przypisuje wartości pola `typ` funkcję tworzącą "
                "obiekt. Metoda `create()` wybiera funkcję na podstawie danych pozycji i zwraca gotowy obiekt "
                "typu `MenuItem`; nieznany typ kończy się wyjątkiem `ValueError` z nazwą tego typu. Metoda "
                "`register()` dopisuje do rejestru nowy rodzaj pozycji.")
    listing(doc, LISTING_FABRYKI, "Listing 2.1. Fabryka pozycji menu (menu/fabryka.py, fragment)")
    akapit(doc, "Role klas we wzorcu:")
    tabela(doc, [
        ("Element", "Rola"),
        ("MenuItemFactory", "fabryka - wybiera i tworzy obiekt na podstawie pola „typ”"),
        ("MenuItem", "wspólny, abstrakcyjny typ obiektów zwracanych przez fabrykę"),
        ("Drink, Dish", "konkretne produkty fabryki; tworzą je funkcje _create_drink i _create_dish"),
        ("load_menu()", "klient fabryki - czyta plik JSON i dla każdej pozycji wywołuje create(); "
                        "nie zna klas Drink i Dish"),
        ("Tavern, app.py", "korzystają z gotowego obiektu Menu; nie tworzą pozycji samodzielnie"),
    ], [4.0, 13.0], pogrubiona_kolumna=0)
    akapit(doc, "Wariant z rejestrem odpowiada problemowi projektu: dane opisują rodzaj pozycji kluczem, więc "
                "potrzebne jest jedno miejsce, które zamienia klucz na klasę. Klasyczna metoda wytwórcza "
                "(Factory Method) wymagałaby hierarchii klas twórców, a w tawernie nie ma naturalnej rodziny "
                "twórców - przy dwóch rodzajach pozycji podklasy fabryki byłyby sztuczne. W Pythonie funkcję "
                "tworzącą można po prostu zapisać w słowniku. Pozostałe rozważane rozwiązania opisuje "
                "punkt 2.4.")
    akapit(doc, "**Co trzeba zmienić, żeby rozszerzyć menu:**")
    punkt(doc, "**nowe danie lub nowa kategoria** - wystarczy dopisać pozycję albo kategorię w pliku "
               "`dane/menu.json`; kod programu się nie zmienia;")
    punkt(doc, "**nowy rodzaj pozycji** (np. zestaw) - nowa podklasa `MenuItem` z własną metodą `kind()` "
               "i rejestracja jej funkcji tworzącej przez `register()` (listing 2.2). Kod fabryki, funkcja "
               "`load_menu()` i interfejs pozostają bez zmian, co jest zgodne z zasadą otwarte-zamknięte "
               "(Open/Closed).")
    listing(doc, LISTING_NOWY_TYP, "Listing 2.2. Dodanie nowego rodzaju pozycji bez zmiany fabryki")
    akapit(doc, "Oba przypadki sprawdzają testy jednostkowe w pliku `test_menu.py`: wczytanie nowej "
                "kategorii z samego pliku JSON oraz rejestracja nowego rodzaju pozycji.")

    # --- 2.3 ---------------------------------------------------------------------
    doc.add_heading("2.3. Oddzielenie logiki od interfejsu", level=2)
    akapit(doc, "Kod jest podzielony na dwie warstwy. Logika aplikacji znajduje się w pakiecie "
                "`czarna_tawerna` i nie importuje biblioteki Streamlit. Interfejs to plik `app.py`, który "
                "tylko wyświetla dane i wywołuje metody klas logiki. Pakiet logiki dzieli się na moduły "
                "odpowiadające rolom w zespole, a zależności między nimi idą w jedną stronę:")
    tabela(doc, [
        ("Moduł", "Zawartość", "Zależy od"),
        ("interfejs", "Tavern - stan sesji kiosku (menu i koszyk)", "zamowienia, menu"),
        ("zamowienia", "Cart, CartItem - koszyk", "menu"),
        ("menu", "MenuItem, Drink, Dish, Category, Menu, MenuItemFactory, load_menu()", "pieniadze"),
        ("pieniadze", "pln() - zamiana złotych na grosze, format_pln() - zapis „14,50 zł”", "-"),
    ], [3.0, 10.5, 3.5], pogrubiona_kolumna=0)
    akapit(doc, "Interfejs korzysta z logiki w następujący sposób:")
    punkt(doc, "przy pierwszym uruchomieniu `app.py` tworzy obiekt `Tavern` i zapisuje go w `st.session_state`. "
               "Streamlit wykonuje skrypt od nowa po każdym kliknięciu, a obiekt w stanie sesji przetrwa "
               "kolejne przeładowania - razem z koszykiem;")
    punkt(doc, "menu wyświetlane jest w zakładkach kategorii na podstawie `tawerna.menu.kategorie`; przy "
               "pozycji widać nazwę, opis, rodzaj (`kind()`) i cenę (`price()`, sformatowaną przez "
               "`format_pln()`);")
    punkt(doc, "przycisk „Do koszyka” wywołuje `tawerna.add_to_cart(id, ilosc)` - interfejs przekazuje tylko "
               "identyfikator pozycji i ilość;")
    punkt(doc, "panel koszyka pokazuje wpisy z `koszyk.pozycje` z wartościami `value()` i sumą `total()`, "
               "a przycisk „Usuń” wywołuje `koszyk.remove(wpis)`.")
    akapit(doc, "Interfejs nie liczy cen i nie sprawdza reguł - robią to klasy logiki. Niedozwolone operacje "
                "(ilość mniejsza niż 1, usunięcie pozycji spoza koszyka, nieznany typ pozycji w pliku) "
                "zgłaszają wyjątek `ValueError`, a brak pozycji o podanym identyfikatorze - `KeyError`. "
                "Interfejs nie dopuszcza do takich sytuacji, np. pole ilości przyjmuje tylko wartości od 1 "
                "do 20. Dzięki temu podziałowi całą logikę można testować bez uruchamiania interfejsu, "
                "a interfejs można by wymienić bez zmian w logice.")

    # --- 2.4 ---------------------------------------------------------------------
    doc.add_heading("2.4. Decyzje projektowe", level=2)
    akapit(doc, "Najważniejszą decyzją etapu był sposób zapisu kwot. Liczby zmiennoprzecinkowe dają błędy "
                "zaokrągleń - w Pythonie `1.10 + 2.20` daje `3.3000000000000003`. Dlatego wszystkie kwoty "
                "są liczbami całkowitymi w groszach: ceny z pliku menu (w złotych) zamienia na grosze funkcja "
                "`pln()`, a złote pojawiają się dopiero przy wyświetlaniu (`format_pln()`). Dodawanie "
                "i mnożenie liczb całkowitych jest dokładne, co potwierdza test dokładności kwot "
                "w pliku `test_zamowienia.py` (1,10 zł + 2,20 zł = 3,30 zł). Pozostałe "
                "decyzje zestawia tabela 2.1.")
    podpis = akapit(doc, "Tabela 2.1. Decyzje projektowe etapu 2", size=Pt(10), italic=True)
    podpis.paragraph_format.keep_with_next = True
    podpis.paragraph_format.space_after = Pt(2)
    tabela(doc, [
        ("Decyzja", "Uzasadnienie", "Rozważane alternatywy"),
        ("Kwoty w groszach (int)", "dokładne obliczenia, prosty typ, łatwe testy",
         "float - błędy zaokrągleń; Decimal - dokładny, ale wymaga pilnowania konwersji przy każdej "
         "operacji"),
        ("Menu w pliku JSON", "zmiana karty bez zmiany kodu",
         "menu zapisane w kodzie - każda zmiana karty to zmiana programu; baza danych - zbędna przy tej "
         "skali"),
        ("Fabryka prosta z rejestrem typów", "jedno miejsce zamienia pole „typ” na klasę; nowe rodzaje "
         "pozycji bez zmiany fabryki",
         "instrukcja if/match w load_menu() - każdy nowy typ zmienia ten kod; Factory Method - sztuczna "
         "hierarchia twórców; Abstract Factory - brak rodzin produktów"),
        ("Klasa abstrakcyjna MenuItem", "wspólny typ dla fabryki, koszyka i interfejsu; nie da się "
         "utworzyć pozycji bez rodzaju",
         "jedna klasa z polem „rodzaj” - rozbudowa wymagałaby instrukcji warunkowych"),
        ("Moduły według ról w zespole, zależności w jedną stronę", "każda osoba ma swój moduł, brak cykli "
         "importów", "jeden moduł logiki; podział według warstw technicznych"),
        ("Koszyk jako lista wpisów (pozycja + ilość)", "każde dodanie to osobny wiersz, który klient może "
         "usunąć; gotowe na pozycje z różnymi dodatkami w kolejnych etapach",
         "słownik identyfikator → ilość - prostszy, ale nie odróżni wariantów tej samej pozycji"),
        ("Stan kiosku w obiekcie Tavern w st.session_state", "koszyk przetrwa przeładowania Streamlit",
         "zmienne globalne modułu - wspólne dla wszystkich użytkowników"),
        ("Nazwy klas i metod po angielsku, pozostałe po polsku", "wymóg konwencji PEP 8 przy zachowaniu "
         "polskich nazw dziedzinowych", "wszystko po polsku - niezgodne z wymaganiami; wszystko po "
         "angielsku - trudniejsze dla zespołu przy nazwach z karty"),
    ], [4.2, 5.8, 7.0], pogrubiona_kolumna=0)

    # --- 2.5 ---------------------------------------------------------------------
    doc.add_heading("2.5. Zrzuty ekranu", level=2)
    akapit(doc, "Rysunek 2.2 przedstawia kiosk: logo tawerny, menu w zakładkach kategorii w postaci kafelków "
                "z grafikami produktów oraz koszyk w panelu bocznym z trzema pozycjami i wartością koszyka.")
    akapit(doc, "Logo tawerny i grafiki produktów wygenerowano modelem AI Nano Banana (Google Gemini). "
                "Grafiki produktów są poglądowe i nie przedstawiają prawdziwych potraw ani napojów. Plik grafiki nazywa się tak jak "
                "identyfikator pozycji w menu, a pozycja bez grafiki dostaje grafikę zastępczą. Pochodzenie "
                "grafik opisuje też plik `ZRODLA.md` w katalogu z grafikami.")
    rysunek(doc, "zrzut_kiosk_menu_koszyk.png", 17.0,
            "Rys. 2.2. Kiosk Czarnej Tawerny - menu i koszyk")
    akapit(doc, "Rysunek 2.3 przedstawia wynik testów jednostkowych. Projekt ma 22 testy w trzech plikach: "
                "`test_menu.py` (menu i fabryka), `test_zamowienia.py` (koszyk i dokładność kwot) oraz "
                "`test_tawerna.py` (stan sesji kiosku). Sześć z nich sprawdza przypadki błędne, a każdy test "
                "porównuje konkretny wynik z oczekiwanym. Wszystkie testy przechodzą.")
    rysunek(doc, "zrzut_pytest.png", 17.0, "Rys. 2.3. Wynik testów jednostkowych (pytest -v)")


def main():
    robocza = "--robocza" in sys.argv
    wyjscie = WYJSCIE_ROBOCZE if robocza else WYJSCIE
    if not robocza and WYJSCIE.exists() and "--nadpisz" not in sys.argv:
        sys.exit(f"{WYJSCIE} już istnieje — może zawierać ręczne poprawki. "
                 f"Uruchom z --nadpisz, żeby wygenerować go od nowa, albo z --robocza.")
    doc = przygotuj_dokument()
    doc.core_properties.title = f"Czarna Tawerna - sprawozdanie, etap {ETAP}"
    doc.core_properties.author = ", ".join(z[0] for z in ZESPOL)
    strona_tytulowa(doc)
    rozdzial_1(doc)
    rozdzial_2(doc)
    doc.save(wyjscie)
    print(wyjscie)


if __name__ == "__main__":
    main()
