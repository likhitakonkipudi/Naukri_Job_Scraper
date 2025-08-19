import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

jobs = []

def scrape_naukri(url):
    print(f"\n🌐 Scraping Naukri: {url}")
    driver.get(url)
    time.sleep(5)

    try:
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple")
        print(f"🔍 Found {len(job_cards)} job cards")

        for card in job_cards:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "a.title")
                title = title_el.text
                link = title_el.get_attribute("href")
            except:
                title, link = None, None

            try:
                company = card.find_element(By.CSS_SELECTOR, "a.subTitle").text
            except:
                company = None

            try:
                location = card.find_element(By.CSS_SELECTOR, ".locWdth").text
            except:
                location = None

            try:
                exp = card.find_element(By.CSS_SELECTOR, ".expwdth").text
            except:
                exp = None

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Experience": exp,
                "Link": link
            })
    except Exception as e:
        print(f"❌ Could not load job cards: {e}")

# ---------------- MAIN ----------------
naukri_url = "https://www.naukri.com/data-engineer-python-spark-aws-sql-jobs-in-india"
scrape_naukri(naukri_url)

driver.quit()

# Save to Excel
if jobs:
    df = pd.DataFrame(jobs)
    df.to_excel("jobs.xlsx", index=False)
    print(f"\n🎉 Done! Saved {len(jobs)} jobs to jobs.xlsx")
else:
    print("\n⚠️ No jobs scraped.")
