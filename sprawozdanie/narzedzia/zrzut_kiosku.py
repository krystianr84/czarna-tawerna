"""Zrzut ekranu kiosku Czarnej Tawerny z kilkoma pozycjami w koszyku."""
import sys
import time

from playwright.sync_api import sync_playwright

URL = "http://localhost:8599"
WYJSCIE = sys.argv[1]


def dodaj(page, zakladka, pozycja, ilosc=1):
    page.get_by_role("tab", name=zakladka).click()
    panel = page.get_by_role("tabpanel").filter(visible=True)
    exp = panel.locator("[data-testid='stVerticalBlock']").filter(has_text=pozycja).last
    if ilosc != 1:
        pole = exp.get_by_label("Ilość")
        pole.fill(str(ilosc))
        pole.press("Enter")
        page.wait_for_timeout(800)
    exp.get_by_role("button", name="Do koszyka").click()
    page.wait_for_timeout(1500)


with sync_playwright() as p:
    przegladarka = p.chromium.launch(channel="msedge", headless=True)
    page = przegladarka.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    for _ in range(30):
        try:
            page.goto(URL)
            break
        except Exception:
            time.sleep(1)
    page.get_by_role("tab", name="Kawy z ładowni").wait_for(timeout=30000)
    dodaj(page, "Kawy z ładowni", "Latte Bosmana", 2)
    dodaj(page, "Prowiant z kambuza", "Tost Kartografa")
    dodaj(page, "Skarby z kufra", "Sernik Gubernatora")
    # widok do zrzutu: zakładka z kawami (kafelki)
    page.get_by_role("tab", name="Kawy z ładowni").click()
    page.wait_for_timeout(1200)
    page.mouse.move(5, 895)
    page.screenshot(path=WYJSCIE)
    print(page.locator("[data-testid='stSidebar']").inner_text().encode("ascii", "replace").decode())
    przegladarka.close()
