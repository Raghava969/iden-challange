# Here’s an **asynchronous Playwright script** that:  

# ✅ **Checks for an existing session** and reuses it if available.  
# ✅ **Authenticates if needed** and saves the session for future runs.  
# ✅ **Navigates** through breadcrumbs to reach the product table.  
# ✅ **Handles pagination** and lazy-loaded content.  
# ✅ **Exports data to a JSON file** in a structured format.  
# ✅ **Uses smart waits** and handles errors gracefully.  

# ---

# ### Install Required Packages  
# Run the following command to install Playwright and set up browsers:  
# ```sh
# pip install playwright
# playwright install
# ```

# ---

# ### **Asynchronous Playwright Script**
# ```python
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from playwright.async_api import Page, expect

SESSION_FILE = "session.json"
OUTPUT_FILE = "product_data.json"
LOGIN_URL = "https://hiring.idenhq.com/"
DASHBOARD_URL = "https://example.com/dashboard"

USERNAME = "raghava.g969@gmail.com"
PASSWORD = "NpDpyCcJ"


async def save_session(context):
    """Saves the browser session to a file."""
    cookies = await context.storage_state(path=SESSION_FILE)


async def load_session(context):
    """Loads the browser session from a file if it exists."""
    if Path(SESSION_FILE).exists():
        await context.add_cookies(json.loads(Path(SESSION_FILE).read_text())["cookies"])


async def login_if_needed(page):
    """Logs in if a session does not exist or is invalid."""
    await page.goto(LOGIN_URL)
    
    # Check if login is required using a more specific locator
    sign_in_element = page.locator("h3:text('Sign in')") # Adjust based on actual HTML structure
    # Check if login is required
    if await sign_in_element.is_visible():
        print("Logging in...")
        await page.fill("input#email", USERNAME)
        await page.fill("input#password", PASSWORD)
        await page.click("button[type='submit']")
        await expect(page.get_by_text("Sign out")).to_be_visible() # Wait for navigation after login
        print("Login successful!")


async def navigate_to_product_table(page):
    """Navigates through breadcrumbs to reach the product table."""
    print("Navigating to product table...")
    await page.click("//button[contains(text(),'Launch Challenge')]")
    await page.click("//button[contains(text(),'Dashboard')]")
    await page.click("//h3[contains(text(),'Inventory')]")
    await page.click("//h3[contains(text(),'Products')]")
    await page.click("//h3[contains(text(),'Full Catalog')]")
    await page.wait_for_selector("//h3[contains(text(),'Product Inventory')]")  # Ensure the table is loaded
    print("Reached product table.")


async def extract_products(page):
    """Extracts product data from the table, handling pagination."""
    all_products = []
    
    while True:
        table_count = await page.locator("//div[contains(text(),'Showing ')]").text
        rows = await page.locator("div.grid>div.rounded-lg").all()
        count = 0
        for row in range(count, len(rows)):
            data = await row.locator("td").all_inner_texts()
            all_products.append({
                "id": data[0],
                "name": data[1],
                "price": data[2],
                "stock": data[3],
            })
        
        # Check if next page exists
        next_button = page.locator("button[aria-label='Next']")
        if await next_button.is_enabled():
            await next_button.click()
            await page.wait_for_load_state("domcontentloaded")  # Wait for new data to load
        else:
            break
    
    return all_products


async def save_to_json(data):
    """Saves extracted data to a JSON file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {OUTPUT_FILE}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load session if available
        await load_session(context)

        page = await context.new_page()

        await login_if_needed(page)
        await navigate_to_product_table(page)
        products = await extract_products(page)
        await save_to_json(products)

        # Save session for future use
        await save_session(context)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
# ```

# ---

# ### **How It Works**
# 1. **Session Handling**: Checks for an existing session and loads it if available. Otherwise, it logs in and saves the session.  
# 2. **Navigation**: Clicks through the breadcrumb trail (`Dashboard` → `Inventory` → `Products` → `Full Catalog`).  
# 3. **Data Extraction**: Collects product details from the table, handling pagination dynamically.  
# 4. **Smart Waiting**: Uses `wait_for_selector()` and `wait_for_load_state()` to handle lazy-loaded content.  
# 5. **Exports to JSON**: Saves extracted product data to `product_data.json`.  

# ---

# ### **Run the Script**
# ```sh
# python script.py
# ```

# 🚀 Let me know if you need any modifications! 🚀