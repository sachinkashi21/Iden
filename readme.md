# Product Scraper Automation

A Python Playwright project to scrape product data from a protected web application.  
The script handles login, session management, dynamic content loading, and exports the scraped data into a structured JSON file.

---

## 📝 Mission Objectives

1. **Session Management**  
   - Checks for an existing session (`session.json`) and restores it to avoid repeated logins.  
   - If no session exists, logs in using the provided credentials and saves the session for future runs.

2. **Navigate Hidden Product Table**  
   - Automates navigation through multiple layers to reach the product table.  
   - Handles dynamically loaded content and pagination.

3. **Data Extraction**  
   - Extracts all product information, including ratings, details, and other attributes.  
   - Handles missing data and dynamically loaded content robustly.

4. **Export to JSON**  
   - Exports scraped data to `products.json` in a clean, structured format for analysis.

5. **Submission**  
   - Designed for submission via a GitHub repository as per platform guidelines.

---

## ⚙️ Project Structure

project/
│── main.py              # Entry point
│── config.py            # Configs & constants
│── auth.py              # Login + session handling
│── session.json         # Saved session storage (ignored in git)
│── products.json        # Scraped product data (ignored in git)
│── scraper/
│    ├── __init__.py
│    ├── utils.py        # JSON file helpers
│    ├── products.py     # Product scraping logic

---

## 🛠 Setup & Installation

1. **Clone the repository**
```
git clone <repo-url>
cd <repo-folder>
```

2. **Create a virtual environment**
```
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. **Install dependencies**
```
pip install playwright
```
*(Ensure `playwright` is installed, and run `playwright install` to install browser binaries)*
```
playwright install
```

4. **Run the script**
```
python main.py
```

---

## 📂 File Details

- **main.py** – Orchestrates login/session and product scraping.  
- **config.py** – Stores constants such as URLs, file paths, and credentials.  
- **auth.py** – Handles login, session saving, and session restoration.  
- **scraper/utils.py** – Helper functions for writing JSON arrays to files.  
- **scraper/products.py** – Contains scraping logic, parsing HTML, handling lazy loading, and writing product data.

---

## ✅ Strategies used for Excellence

- Smart waiting for elements before interaction using `wait_for_function` and `wait_for_load_state`.  
- Handles lazy-loaded content and pagination robustly.  
- Graceful error handling during scraping and parsing.  
- Modular code for maintainability and clarity.  
- Session persistence avoids repeated logins, making the script faster on subsequent runs.

---

## ⚠️ Notes

- `session.json` and `products.json` are runtime-generated files and are ignored in `.gitignore`.  
- Run in **headed mode** (`headless=False`) for debugging and visual verification; switch to headless for automated runs.

---

## 📈 Output Example

`products.json` will be a JSON array of product objects like:

```
[
{"name": "Premium Sports Lite", "Rating": 1.0, "ID": "19", "Manufacturer": "QualityCraft", "Guarantee": "1 Year", "Rating": 3.0},
{"name": "Premium Sports Lite", "Rating": 3.0, "ID": "0", "Manufacturer": "ValueCreators", "Guarantee": "6 Months", "Rating": 4.5}
]
```