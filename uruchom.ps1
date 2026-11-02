# Uruchamia aplikację Czarna Tawerna z Pythona w .venv - bez ręcznej aktywacji środowiska.
#
# Użycie (z dowolnego folderu):  & "C:\...\Projekt\uruchom.ps1"
# W folderze projektu:           .\uruchom.ps1
# Dodatkowe argumenty trafiają do streamlit, np.  .\uruchom.ps1 --server.port 8502

$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "Brak środowiska .venv w $PSScriptRoot" -ForegroundColor Red
    Write-Host "Utwórz je poleceniami:"
    Write-Host "  python -m venv .venv"
    Write-Host "  .venv\Scripts\python -m pip install -r requirements.txt"
    exit 1
}

# streamlit szuka dane/menu.json względem app.py, ale katalog roboczy ustawiamy na projekt dla porządku
Push-Location $PSScriptRoot
try {
    & $python -m streamlit run app.py @args
} finally {
    Pop-Location
}
