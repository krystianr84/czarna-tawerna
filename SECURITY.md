# Polityka bezpieczeństwa

## Wspierane wersje

Czarna Tawerna to projekt edukacyjny rozwijany na jednej gałęzi. Poprawki bezpieczeństwa trafiają tylko do najnowszej wersji na gałęzi `main`.

| Wersja | Wsparcie |
|---|---|
| `main` (bieżący etap) | ✅ |
| starsze commity i oddane archiwa ZIP | ❌ |

## Zakres

Aplikacja działa lokalnie jako kiosk (Streamlit) i nie przechowuje danych osobowych, haseł ani płatności - koszyk istnieje tylko w pamięci sesji przeglądarki. Za problem z bezpieczeństwem uznajemy m.in.:

- sekrety (klucze, tokeny, hasła) przypadkowo dodane do repozytorium,
- dane osobowe (np. numery albumów, adresy e-mail) w plikach, które nie powinny ich zawierać,
- podatności w zależnościach z `requirements.txt`,
- możliwość wykonania cudzego kodu lub odczytu plików spoza projektu przez interfejs kiosku.

## Jak zgłosić problem

**Nie zakładaj publicznego issue** dla problemu z bezpieczeństwem.

1. Napisz bezpośrednio do kierownika projektu - Krystiana Rutkowskiego (konto GitHub: [krystianr84](https://github.com/krystianr84)) - albo użyj opcji **Security → Report a vulnerability**, jeśli jest dostępna w repozytorium.
2. Opisz problem, kroki do odtworzenia i pliki, których dotyczy.
3. Odpowiemy w ciągu kilku dni roboczych i ustalimy poprawkę z osobą odpowiedzialną za dany obszar.

Jeśli do repozytorium trafił sekret, samo usunięcie pliku nie wystarczy - sekret trzeba unieważnić (np. wygenerować nowy token), bo zostaje w historii Gita.
