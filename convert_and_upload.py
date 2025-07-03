import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

CSV_FILE = 'genai_jobs_results.csv'
EXCEL_FILE = 'genai_jobs_results.xlsx'
GOOGLE_SHEET_NAME = 'linkedinjobsCsv'  # <-- Change this to your actual Google Sheet name
CREDENTIALS_FILE = 'credentials.json'

# Convert CSV to Excel
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df = df.fillna('')  # Replace NaN with empty string
    df.to_excel(EXCEL_FILE, index=False)
    print(f"[INFO] Saved Excel file: {EXCEL_FILE}")
else:
    print(f"[ERROR] CSV file not found: {CSV_FILE}")
    df = None

# Upload to Google Sheets
if df is not None and os.path.exists(CREDENTIALS_FILE):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(creds)
    try:
        spreadsheet = client.open(GOOGLE_SHEET_NAME)
        worksheet = spreadsheet.sheet1  # or use .worksheet('SheetName')
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"[INFO] Uploaded data to Google Sheet: {GOOGLE_SHEET_NAME}")
    except Exception as e:
        print(f"[ERROR] Could not upload to Google Sheets: {e}")
else:
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] Google API credentials file not found: {CREDENTIALS_FILE}") 