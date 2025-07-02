import os
import json
from linkedin_scraper import Job, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
load_dotenv()
# Use headless mode to avoid opening a browser window
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Specify ChromeDriver path using Service
#service = Service("D:\versa\project_Files\linkedin_scraper\chromedriver-win64\chromedriver.exe")
service = Service("D:/versa/project_Files/linkedin_scraper/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Login using environment variables
email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")
if not email or not password:
    raise ValueError("LINKEDIN_USER or LINKEDIN_PASSWORD environment variables not set")
actions.login(driver, email, password)

# Update the job search URL for GenAI, entry-level, remote, all job types, Germany
job_search_url = (
    "https://www.linkedin.com/jobs/search/"
    "?keywords=genai%20OR%20generative%20ai%20OR%20llm%20OR%20ai%20engineer%20OR%20career%20change%20OR%20transition%20OR%20medicine%20OR%20management%20OR%20junior%20OR%20trainee%20OR%20open%20to%20learning%20OR%20no%20prior%20experience%20OR%20self-taught%20OR%20bootcamp"
    "&geoId=101282230"
    "&f_E=1,2"
    "&f_WT=2"  # Remote jobs
    "&f_TPR=r604800"  # Past week
    "&sortBy=DD"  # Newest first
)
print(f"[DEBUG] Using job search URL: {job_search_url}")
driver.get(job_search_url)

# CAPTCHA/verification check
if "captcha" in driver.page_source.lower() or "verify" in driver.page_source.lower():
    print("[DEBUG] CAPTCHA or verification detected! You may need to solve it manually in the browser window.")

# Debug: Print page title and a snippet of the page source
print("[DEBUG] Page title:", driver.title)
print("[DEBUG] Page source snippet:", driver.page_source[:1000])

# Wait for job cards to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.base-card__full-link"))
    )
    print("[DEBUG] Job cards loaded.")
except Exception as e:
    print(f"[DEBUG] Timeout waiting for job cards: {e}")

# Extract job URLs from the search results page
job_urls = []
try:
    # Find job cards (updated selector based on LinkedIn's HTML structure)
    job_cards = driver.find_elements(By.CSS_SELECTOR, "a.ember-view[href^='/jobs/view/']")
    for card in job_cards:
        href = card.get_attribute("href")
        if href:
            if href.startswith("/jobs/view/"):
                job_urls.append("https://www.linkedin.com" + href)
            else:
                job_urls.append(href)
    job_urls = list(dict.fromkeys(job_urls))  # Remove duplicates
    print(f"[DEBUG] Found {len(job_urls)} job URLs: {job_urls}")
except Exception as e:
    print(json.dumps({"error": f"Failed to extract job URLs: {str(e)}"}))
    driver.quit()
    exit()

# Expanded keywords for GenAI, career change, and related fields
required_skills = [
    "genai", "generative ai", "llm", "ai engineer", "ai developer", "machine learning", "deep learning", "nlp", "large language model", "llmops", "prompt engineering", "rag", "openai", "career change", "transition", "open to learning", "no prior experience", "self-taught", "bootcamp", "medicine", "management", "junior", "trainee", "intern", "entry level", "fresher", "graduate", "data science", "data scientist", "mlops", "artificial intelligence", "chatgpt", "gpt", "bert", "transformer", "remote", "quereinsteiger", "umsteiger", "neueinsteiger", "querdenker", "autodidakt", "umschulung", "weiterbildung", "reskill", "upskill"
]

def extract_contact_details(text):
    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    # Extract phone (international and local formats)
    phone_match = re.search(r"(\+\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}", text)
    # Extract contact person (common patterns)
    contact_match = re.search(r"(?:contact(?: person)?|ansprechpartner(?:in)?|kontakt(?:person)?|reach out to|apply to)[:\s]*([A-ZÄÖÜ][a-zäöüßA-ZÄÖÜ .'-]+)", text, re.IGNORECASE)
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "contact_person": contact_match.group(1).strip() if contact_match else None
    }

# Scrape each job and filter by skills
matching_jobs = []
results_count = 0
max_results = 50
page_size = 25  # LinkedIn default page size
start = 0

while results_count < max_results:
    paginated_url = job_search_url + f"&start={start}"
    print(f"[DEBUG] Fetching page starting at result {start}")
    driver.get(paginated_url)

    # Wait for job cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.ember-view[href^='/jobs/view/']"))
        )
        print("[DEBUG] Job cards loaded.")
    except Exception as e:
        print(f"[DEBUG] Timeout waiting for job cards: {e}")

    # Extract job URLs from the search results page
    job_urls = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, "a.ember-view[href^='/jobs/view/']")
    for card in job_cards:
        href = card.get_attribute("href")
        if href:
            if href.startswith("/jobs/view/"):
                job_urls.append("https://www.linkedin.com" + href)
            else:
                job_urls.append(href)
    job_urls = list(dict.fromkeys(job_urls))  # Remove duplicates
    print(f"[DEBUG] Found {len(job_urls)} job URLs: {job_urls}")

    for url in job_urls:
        if results_count >= max_results:
            break
        try:
            job = Job(url, driver=driver, close_on_complete=False)
            description = job.job_description.lower() if isinstance(job.job_description, str) else str(job.job_description).lower()
            print(f"[DEBUG] Scraping job: {url}\nDescription: {description[:200]}...")
            skills_found = any(skill.lower() in description for skill in required_skills)
            if skills_found:
                contact_details = extract_contact_details(job.job_description)
                data = {
                    "title": job.job_title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.job_description,
                    "url": url,
                    "email": contact_details["email"],
                    "phone": contact_details["phone"],
                    "contact_person": contact_details["contact_person"]
                }
                matching_jobs.append(data)
                results_count += 1
        except Exception as e:
            print(json.dumps({"error": f"Failed to scrape job {url}: {str(e)}"}))
            continue
    if len(job_urls) < page_size:
        break  # No more pages
    start += page_size

# Output matching jobs as JSON and save to file
if matching_jobs:
    print(json.dumps(matching_jobs, indent=2, ensure_ascii=False))

    # --- JSON APPEND LOGIC ---
    json_path = "genai_jobs_results.json"
    existing_json = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                existing_json = json.load(f)
            except Exception:
                existing_json = []
    # Avoid duplicates by URL
    existing_urls = {job.get("url") for job in existing_json}
    new_jobs_json = [job for job in matching_jobs if job.get("url") not in existing_urls]
    all_jobs_json = existing_json + new_jobs_json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_jobs_json, f, ensure_ascii=False, indent=2)

    # --- CSV APPEND LOGIC ---
    csv_fields = ["title", "company", "location", "description", "url", "email", "phone", "contact_person"]
    csv_path = "genai_jobs_results.csv"
    existing_urls_csv = set()
    file_exists = os.path.exists(csv_path)
    if file_exists:
        with open(csv_path, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_urls_csv.add(row.get("url"))
    new_jobs_csv = [job for job in matching_jobs if job.get("url") not in existing_urls_csv]
    write_header = not file_exists or os.stat(csv_path).st_size == 0
    with open(csv_path, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        if write_header:
            writer.writeheader()
        for job in new_jobs_csv:
            writer.writerow(job)
    print("[DEBUG] Results appended to genai_jobs_results.csv and genai_jobs_results.json")
else:
    print(json.dumps({"error": "No jobs found matching all required skills"}))

# Keep browser open until user input (for debugging)
#input("Press Enter to close the browser")
driver.quit()