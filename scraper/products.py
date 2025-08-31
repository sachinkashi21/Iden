from playwright.sync_api import Page, TimeoutError
from config import PRODUCTS_FILE
from .utils import open_file, append_to_file, close_file
import re

import re

def extract_product_data_html(product_html: str) -> dict:
    name_match = re.search(r'<div class="h-12[^"]*"[^>]*>(.*?)</div>', product_html, re.DOTALL)
    name = name_match.group(1).strip() if name_match else "Unknown"

    details = {}
    rows = re.findall(r'<div class="flex items-center[^"]*"[^>]*>(.*?)</div>', product_html, re.DOTALL)
    # details["Rating"]=3.0
    for row in rows:
        spans = re.findall(r'<span[^>]*>(.*?)</span>', row, re.DOTALL)
        if len(spans) >= 2:
            key = spans[0].strip().replace(":", "").replace(" ", "_")
            if key.lower() == "rating":
                m = re.search(r'<span[^>]*>\s*(\d+(?:\.\d+)?)\s*</span>', row, re.DOTALL)
                if m:
                    details[key] = float(m.group(1))
                    continue

                label = re.search(r'<span[^>]*>\s*Rating\s*</span>', product_html, re.IGNORECASE)
                if label:
                    window = product_html[label.end(): label.end() + 600]  # small window after the label
                    m2 = re.search(r'<span[^>]*>\s*(\d+(?:\.\d+)?)\s*</span>', window, re.DOTALL)
                    if m2:
                        details[key] = float(m2.group(1))
                        continue

                    star_count = len(re.findall(r'<svg[^>]*(?:fill-[^">]*yellow|text-yellow)[^>]*>', window, re.IGNORECASE))
                    details[key] = float(star_count) if star_count > 0 else None
                else:
                    details[key] = None
            else:
                details[key] = spans[1].strip()

    return {"name": name, **details}



def scrape_products(page: Page) -> None:
    open_file(PRODUCTS_FILE)
    first_write = True

    try:
        page.get_by_role("button", name="Launch Challenge").click()
        page.wait_for_load_state("networkidle")

        total = int(
            page.locator("div.text-sm.text-muted-foreground span.font-medium.text-foreground")
            .nth(1)
            .inner_text()
            .strip()
        )
        print(f"📦 Total {total} products")

        processed, seen_ids = 0, set()

        while processed < total:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            try:
                page.wait_for_function(
                    "expected => document.querySelectorAll('div.rounded-lg.border.bg-card').length > expected",
                    arg=processed,
                    timeout=10000,
                )
            except TimeoutError:
                print("⚠️ Timeout waiting for new products, retrying scroll...")
                continue

            new_product_htmls = page.eval_on_selector_all(
                f"div.rounded-lg.border.bg-card:nth-child(n+{processed+1})",
                "els => els.map(el => el.innerHTML)"
            )

            new_data = []
            for product_html in new_product_htmls:
                try:
                    data = extract_product_data_html(product_html)
                    pid = data.get("ID") or data.get("id")
                    if pid and pid not in seen_ids:
                        new_data.append(data)
                        seen_ids.add(pid)
                except Exception as e:
                    print(f"⚠️ Error parsing product: {e}")

            if new_data:
                append_to_file(PRODUCTS_FILE, new_data, first=first_write)
                first_write = False
                processed += len(new_data)
                print(f"\n✅ Saved {processed}/{total}", end="")
            else:
                # Scroll a bit up if no new products loaded
                page.evaluate("window.scrollBy(0, -300)")
                print(".", end="")

    finally:
        close_file(PRODUCTS_FILE)
        print(" File closed")

    print("\n🎉 Scraping completed")
