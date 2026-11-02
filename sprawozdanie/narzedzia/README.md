# Narzędzia do zasobów sprawozdania

Generują obrazki w `sprawozdanie/zasoby/`. Nie wchodzą do ZIP-a (to narzędzia, nie kod aplikacji).
Wymagają w `.venv`: `playwright` (steruje zainstalowanym Edge, bez pobierania przeglądarek) oraz Mermaid CLI (`mmdc`, npm).

Uruchamiać z katalogu projektu:

```powershell
# diagram klas etapu 2 (kod Mermaid wycięty z design.md do .mmd)
mmdc -i sprawozdanie/zasoby/diagram_klas_etap2.mmd -o sprawozdanie/zasoby/diagram_klas_etap2.png -b white -s 3 -c sprawozdanie/narzedzia/mermaid.json

# zrzut kiosku: najpierw w osobnym terminalu
.venv\Scripts\python -m streamlit run app.py --server.headless true --server.port 8599
.venv\Scripts\python sprawozdanie/narzedzia/zrzut_kiosku.py sprawozdanie/zasoby/zrzut_kiosk_menu_koszyk.png

# obraz wyniku pytest -v (prawdziwe wyjście polecenia)
.venv\Scripts\python sprawozdanie/narzedzia/zrzut_testow.py "$PWD" sprawozdanie/zasoby/zrzut_pytest.png
```
