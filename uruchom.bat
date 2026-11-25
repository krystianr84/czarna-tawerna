@echo off
rem Uruchamia Czarną Tawernę dwuklikiem (Windows).
rem Przy pierwszym uruchomieniu tworzy .venv i instaluje biblioteki.
rem Dodatkowe argumenty trafiają do streamlit.
setlocal
chcp 65001 >nul
title Czarna Tawerna
cd /d "%~dp0"
set "PY=.venv\Scripts\python.exe"
set "ZNACZNIK=.venv\requirements.zainstalowane.txt"

if exist "%PY%" goto sprawdz_venv

set "BAZA=py -3"
%BAZA% -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 goto utworz
set "BAZA=python"
%BAZA% -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 goto utworz
echo Nie znaleziono Pythona 3.10 lub nowszego.
echo Zainstaluj go ze strony https://www.python.org/downloads/
echo i zaznacz w instalatorze opcję "Add python.exe to PATH".
goto blad

:utworz
echo Tworzę środowisko .venv...
%BAZA% -m venv .venv
if errorlevel 1 goto blad

:sprawdz_venv
"%PY%" -m pip --version >nul 2>&1
if not errorlevel 1 goto biblioteki
echo Środowisko .venv jest uszkodzone lub przeniesione z innego komputera.
echo Usuń folder .venv i uruchom skrypt ponownie.
goto blad

:biblioteki
fc /b requirements.txt "%ZNACZNIK%" >nul 2>&1
if not errorlevel 1 goto start
echo Instaluję biblioteki, to może potrwać kilka minut...
"%PY%" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto blad
copy /y requirements.txt "%ZNACZNIK%" >nul

:start
echo Uruchamiam kiosk. Zatrzymanie: Ctrl+C albo zamknięcie okna.
"%PY%" -m streamlit run app.py --server.showEmailPrompt false %*
if errorlevel 1 goto blad
exit /b 0

:blad
echo.
echo Nie udało się uruchomić projektu - zob. komunikat powyżej.
pause
exit /b 1
