import schedule
import time
import subprocess
import sys
import os


def job():
    # Use sys.executable to ensure the venv's Python is used
    script_path = os.path.join(os.getcwd(), "scrape_job.py")
    subprocess.run([sys.executable, script_path])
    # Run the CSV to Sheets/Excel conversion after scraping
    convert_script = os.path.join(os.getcwd(), "convert_and_upload.py")
    subprocess.run([sys.executable, convert_script])

schedule.every(1).hours.do(job)
#schedule.every(5).minutes.do(job)
#schedule.every(15).minutes.do(job)
#schedule.every(30).minutes.do(job)
#schedule.every(45).minutes.do(job)
#schedule.every(60).minutes.do(job)
#schedule.every(90).minutes.do(job)
#schedule.every(120).minutes.do(job)
#schedule.every(180).minutes.do(job)

print("Scheduler started. The script will run every 1 hours.")
job()  # Run once at start (optional, remove if not needed)

while True:
    schedule.run_pending()
    time.sleep(60) 