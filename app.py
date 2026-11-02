"""Interfejs Streamlit Czarnej Tawerny - etap 2: menu i koszyk.

Uruchomienie:  streamlit run app.py
"""

from pathlib import Path

import streamlit as st

from czarna_tawerna.interfejs import Tavern
from czarna_tawerna.pieniadze import format_pln

PLIK_MENU = Path(__file__).parent / "dane" / "menu.json"
KATALOG_ZDJEC = Path(__file__).parent / "dane" / "zdjecia"
LOGO = KATALOG_ZDJEC / "Czrna_tawerna_logo1.jpg"  # baner tawerny na górze kiosku


def photo_path(id_pozycji: str) -> Path:
    """Zdjęcie poglądowe pozycji albo grafika zastępcza, gdy go brak."""
    zdjecie = KATALOG_ZDJEC / f"{id_pozycji}.jpg"
    return zdjecie if zdjecie.exists() else KATALOG_ZDJEC / "brak.jpg"


st.set_page_config(page_title="Czarna Tawerna", page_icon="🏴‍☠️", layout="wide")

# obiekt tawerny żyje w sesji, żeby koszyk przetrwał przeładowania
if "tawerna" not in st.session_state:
    st.session_state.tawerna = Tavern(PLIK_MENU)
tawerna: Tavern = st.session_state.tawerna

with st.container(horizontal_alignment="center"):
    st.image(LOGO, width=720, alt="Czarna Tawerna - kawiarnia")
st.caption('<span style="font-size: 250%">'
           "Wybierz kategorię i pozycję z menu, a potem dodaj ją do koszyka.</span>",
           unsafe_allow_html=True, text_alignment="center")

# --- menu -------------------------------------------------------------
SZEROKOSC_KAFELKA = 310  # px; kafelki zawijają się do kolejnych rzędów

zakladki = st.tabs([k.nazwa for k in tawerna.menu.kategorie])
for zakladka, kategoria in zip(zakladki, tawerna.menu.kategorie):
    with zakladka, st.container(horizontal=True):
        for pozycja in kategoria.pozycje:
            with st.container(border=True, width=SZEROKOSC_KAFELKA, height="stretch"):
                st.image(photo_path(pozycja.id), width="stretch", alt=pozycja.nazwa)
                st.markdown(f"**{pozycja.nazwa}**")
                st.caption(f"{pozycja.opis} · {pozycja.kind()}")
                if pozycja.oznaczenia:
                    st.caption(", ".join(sorted(pozycja.oznaczenia)))
                st.space("stretch")  # cena i przycisk zawsze na dole kafelka
                st.markdown(f"### {format_pln(pozycja.price())}")
                with st.container(horizontal=True, vertical_alignment="center"):
                    st.markdown("Ilość", width="content")
                    ilosc = st.number_input("Ilość", min_value=1, max_value=20, value=1,
                                            key=f"i_{pozycja.id}",
                                            label_visibility="collapsed")
                etykieta = f"Do koszyka - {format_pln(pozycja.price() * ilosc)}"
                if st.button(etykieta, key=f"b_{pozycja.id}", width="stretch"):
                    tawerna.add_to_cart(pozycja.id, ilosc)
                    st.rerun()

# --- koszyk -----------------------------------------------------------
with st.sidebar:
    st.header("🧺 Koszyk")
    if tawerna.koszyk.is_empty():
        st.write("Koszyk jest pusty.")
    for i, wpis in enumerate(tawerna.koszyk.pozycje):
        st.write(f"{wpis.ilosc} × {wpis.pozycja.nazwa} "
                 f"({format_pln(wpis.pozycja.price())}) - **{format_pln(wpis.value())}**")
        if st.button("Usuń", key=f"usun_{i}", help="Usuń z koszyka"):
            tawerna.koszyk.remove(wpis)
            st.rerun()
    st.divider()
    st.subheader(f"Wartość koszyka: {format_pln(tawerna.koszyk.total())}")
