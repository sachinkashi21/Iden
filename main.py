from playwright.sync_api import sync_playwright
from auth import load_session, login
from scraper.products import scrape_products

def main():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            if not load_session(page):
                login(page)

            scrape_products(page)
            browser.close()
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
