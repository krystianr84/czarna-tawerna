"""Obraz wyniku `pytest -v` (prawdziwe wyjście polecenia) w stylu okna terminala."""
import html
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJEKT = Path(sys.argv[1])
WYJSCIE = sys.argv[2]
POLECENIE = "pytest -v"

wynik = subprocess.run([str(PROJEKT / ".venv/Scripts/python.exe"), "-m", "pytest", "-v", "-p", "no:cacheprovider"],
                       cwd=PROJEKT, capture_output=True, text=True, encoding="utf-8",
                       env={"PYTHONIOENCODING": "utf-8", "SYSTEMROOT": "C:\\Windows", "COLUMNS": "110"})
tekst = wynik.stdout.rstrip()
if wynik.returncode != 0:
    sys.exit("pytest nie przeszedł:\n" + tekst)

linie = []
for linia in tekst.splitlines():
    e = html.escape(linia)
    e = re.sub(r"(PASSED)", r'<span class="ok">\1</span>', e)
    e = re.sub(r"(\[\s*\d+%\])", r'<span class="pr">\1</span>', e)
    if re.match(r"=+ \d+ passed", linia):
        e = f'<span class="okb">{e}</span>'
    linie.append(e)

strona = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ margin: 0; background: #fff; }}
.okno {{ width: 1180px; margin: 16px; border-radius: 8px; overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,.25); font-family: Consolas, monospace; }}
.belka {{ background: #2d2d2d; color: #ccc; padding: 7px 12px; font: 13px "Segoe UI", sans-serif; }}
pre {{ margin: 0; padding: 12px 14px; background: #0c0c0c; color: #cccccc; font-size: 13px;
       line-height: 1.35; white-space: pre; }}
.ok {{ color: #16c60c; }} .okb {{ color: #16c60c; font-weight: bold; }} .pr {{ color: #61d6d6; }}
.prompt {{ color: #f9f1a5; }}
</style></head><body><div class="okno"><div class="belka">Terminal - Czarna Tawerna</div>
<pre><span class="prompt">PS {html.escape(str(PROJEKT))}&gt;</span> {POLECENIE}
{chr(10).join(linie)}</pre></div></body></html>"""

with sync_playwright() as p:
    przegladarka = p.chromium.launch(channel="msedge", headless=True)
    page = przegladarka.new_page(device_scale_factor=1.5)
    page.set_content(strona)
    page.locator(".okno").screenshot(path=WYJSCIE)
    przegladarka.close()
print(tekst.splitlines()[-1])
