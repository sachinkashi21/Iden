import os, json
from playwright.sync_api import Page, Error
from config import URL, SESSION_FILE, EMAIL, PASSWORD

def save_session(page: Page) -> None:
    session_data = page.evaluate("() => Object.entries(sessionStorage)")
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session_data, f)
    print("💾 Session saved")

def load_session(page: Page) -> bool:
    if not os.path.exists(SESSION_FILE):
        return False
    try:
        page.goto(URL, wait_until="load")
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)

        page.evaluate(
            """(data) => {
                for (const [k, v] of data) sessionStorage.setItem(k, v);
            }""",
            session_data,
        )
        page.reload(wait_until="load")
        page.wait_for_url(URL + "instructions", timeout=15000)
        print("🔑 Session restored")
        return True
    except Exception as e:
        print(f"⚠️ Session load failed: {e}")
        return False


def login(page: Page) -> None:
    try:
        page.goto(URL, wait_until="load")
        page.fill("input[type='email']", EMAIL)
        page.fill("input[type='password']", PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_url(URL + "instructions", timeout=15000)
        save_session(page)
        print("✅ Login successful")
    except Error as e:
        print(f"❌ Login failed: {e}")
        raise
