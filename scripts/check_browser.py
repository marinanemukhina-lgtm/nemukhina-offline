"""Chromium integration checks with synthetic files; does not evaluate a real model.

CI-only dependency: playwright==1.56.0. The app itself remains standard-library-only.
Everything runs in a temporary copy, never in the user's model folders or database.
"""

import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(os.environ.get("BROWSER_CHECK_OUTPUT", "browser-check-artifacts")).resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory(prefix="nemukhina-ui-") as temporary:
    app = Path(temporary)
    for name in ("offline.py", "library.py", "conversations.py", "model_setup.py", "server.py"):
        shutil.copy2(ROOT / name, app / name)
    shutil.copytree(ROOT / "web", app / "web")
    runtime, models = app / "runtime" / "synthetic", app / "models"
    runtime.mkdir(parents=True)
    models.mkdir()
    engine = runtime / "llama-completion"
    engine.write_text(
        "#!/usr/bin/env python3\n"
        "import sys, time\n"
        "model = sys.argv[sys.argv.index('-m') + 1]\n"
        "if 'slow' in model: time.sleep(10)\n"
        "print('4')\n", encoding="utf-8"
    )
    engine.chmod(0o700)
    model = models / "synthetic.gguf"
    model.write_bytes(b"GGUF synthetic fixture, not real weights")
    slow_model = models / "slow.gguf"
    slow_model.write_bytes(b"GGUF slow fixture, not real weights")
    process = subprocess.Popen(
        [sys.executable, str(app / "server.py"), "--port", "0", "--db", str(app / "test.db")],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=app,
    )
    lines = queue.Queue()
    threading.Thread(target=lambda: lines.put(process.stdout.readline()), daemon=True).start()
    try:
        line = lines.get(timeout=15)
        if "http://127.0.0.1:" not in line:
            raise AssertionError("Local server did not start: " + line)
        origin = line.strip().split()[-1]
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1024}, reduced_motion="reduce")
            errors, external = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            def local_only(route):
                if route.request.url.startswith(origin + "/"):
                    route.continue_()
                else:
                    external.append(route.request.url)
                    route.abort()
            page.route("**/*", local_only)
            try:
                page.goto(origin)
                expect(page.locator("#modelHint")).to_contain_text("локальная модель")
                page.locator("#question").fill("Синтетический вопрос для проверки интерфейса")
                page.locator("#send").click()
                expect(page.locator("#settingsDialog")).to_be_visible()
                expect(page.locator("#question")).to_have_value("Синтетический вопрос для проверки интерфейса")
                page.locator("#discoverModels").click()
                expect(page.locator("#discoveredModels")).to_be_visible()
                page.locator("#engineChoice").select_option(str(engine))
                page.locator("#modelChoice").select_option(str(model))
                page.locator("#modelForm button").click()
                expect(page.locator("#probeSummary")).to_contain_text("ответила на контрольный вопрос", timeout=15000)
                expect(page.locator("#probeAnswer")).to_have_text("4")
                page.screenshot(path=str(OUTPUT / "setup-desktop.png"))
                page.locator("#settingsDialog .close").click()
                expect(page.locator("#modelHint")).to_contain_text("прошла проверку")
                page.locator("#history").click()
                expect(page.locator("#historyList")).to_contain_text("Здесь появятся")
                page.locator("#historyDialog .close").click()
                page.locator("#settings").click()
                page.locator("#modelPath").fill(str(slow_model))
                page.locator("#modelForm button").click()
                expect(page.locator("#cancelCheck")).to_be_visible()
                page.locator("#cancelCheck").click()
                expect(page.locator("#settingsStatus")).to_contain_text(re.compile("останов", re.I), timeout=15000)
                expect(page.locator("#probeResult")).to_be_hidden()
                expect(page.locator("#modelForm button")).to_be_enabled()
                page.locator("#modelPath").fill(str(model))
                page.locator("#modelForm button").click()
                expect(page.locator("#probeSummary")).to_contain_text("ответила на контрольный вопрос", timeout=15000)
                page.locator("#settingsDialog .close").click()
                page.locator("#send").click()
                expect(page.locator("#answer")).to_have_text("4", timeout=15000)
                for language in ("ru", "en", "zh"):
                    page.set_viewport_size({"width": 390, "height": 844})
                    page.locator("#lang").select_option(language)
                    page.locator("#settings").click()
                    expect(page.locator("#settingsDialog")).to_be_visible()
                    sizes = page.locator("#settingsDialog").evaluate(
                        "(el) => ({scroll:el.scrollWidth, client:el.clientWidth})"
                    )
                    assert sizes["scroll"] <= sizes["client"] + 1, (language, sizes)
                    page.screenshot(path=str(OUTPUT / ("setup-mobile-" + language + ".png")))
                    page.locator("#settingsDialog .close").click()
                assert not errors, errors
                assert not external, external
                print("PASS: model discovery, setup, real HTTP/process round-trip with synthetic engine, cancellation, retry, history isolation, RU/EN/ZH mobile widths, no external requests.")
            except Exception:
                page.screenshot(path=str(OUTPUT / "failure.png"))
                raise
            finally:
                browser.close()
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
