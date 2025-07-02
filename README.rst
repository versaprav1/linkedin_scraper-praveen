.. role:: raw-html-m2r(raw)
   :format: html


Linkedin Scraper
================

Scrapes Linkedin User Data

`Linkedin Scraper <#linkedin-scraper>`_


* `Installation <#installation>`_
* `Setup <#setup>`_
* `Usage <#usage>`_

  * `Sample Usage <#sample-usage>`_
  * `User Scraping <#user-scraping>`_
  * `Company Scraping <#company-scraping>`_
  * `Job Scraping <#job-scraping>`_
  * `Job Search Scraping <#job-search-scraping>`_
  * `Scraping sites where login is required first <#scraping-sites-where-login-is-required-first>`_
  * `Scraping sites and login automatically <#scraping-sites-and-login-automatically>`_

* `API <#api>`_

  * `Person <#person>`_

    * `\ ``linkedin_url`` <#linkedin_url>`_
    * `\ ``name`` <#name>`_
    * `\ ``about`` <#about>`_
    * `\ ``experiences`` <#experiences>`_
    * `\ ``educations`` <#educations>`_
    * `\ ``interests`` <#interests>`_
    * `\ ``accomplishment`` <#accomplishment>`_
    * `\ ``company`` <#company>`_
    * `\ ``job_title`` <#job_title>`_
    * `\ ``driver`` <#driver>`_
    * `\ ``scrape`` <#scrape>`_
    * `\ ``scrape(close_on_complete=True)`` <#scrapeclose_on_completetrue>`_

  * `Company <#company>`_

    * `\ ``linkedin_url`` <#linkedin_url-1>`_
    * `\ ``name`` <#name-1>`_
    * `\ ``about_us`` <#about_us>`_
    * `\ ``website`` <#website>`_
    * `\ ``headquarters`` <#headquarters>`_
    * `\ ``founded`` <#founded>`_
    * `\ ``company_type`` <#company_type>`_
    * `\ ``company_size`` <#company_size>`_
    * `\ ``specialties`` <#specialties>`_
    * `\ ``showcase_pages`` <#showcase_pages>`_
    * `\ ``affiliated_companies`` <#affiliated_companies>`_
    * `\ ``driver`` <#driver-1>`_
    * `\ ``get_employees`` <#get_employees>`_
    * `\ ``scrape(close_on_complete=True)`` <#scrapeclose_on_completetrue-1>`_

* `Contribution <#contribution>`_

Advanced GenAI Job Scraping (Entry-Level, Career Change, Remote)
----------------------------------------------------------------

This project now includes an advanced script for scraping GenAI and related jobs on LinkedIn, especially for people transitioning into the field (career changers, high experience in other fields, entry-level in GenAI).

Features
^^^^^^^^
- Scrapes LinkedIn jobs using a broad set of GenAI and career change keywords (including German terms)
- Filters for entry-level and internship jobs, remote, and Germany (customizable)
- Paginates through results (up to 50 jobs per run)
- Extracts job title, company, location, description, URL, and attempts to extract email, phone, and contact person from the job description
- Saves results to both JSON and CSV for easy analysis
- Handles LinkedIn CAPTCHA/verification (manual intervention required)

Usage
^^^^^
1. Set your LinkedIn credentials as environment variables or in a `.env` file::

   LINKEDIN_USER=your_email@example.com
   LINKEDIN_PASSWORD=your_password

2. Run the script::

   python scrape_job.py

3. If prompted, solve any CAPTCHA in the browser window.
4. Results will be saved to ``genai_jobs_results.json`` and ``genai_jobs_results.csv`` in the project root.

Customization
^^^^^^^^^^^^^
- **Keywords:** Edit the ``required_skills`` list in ``scrape_job.py`` to add/remove keywords for your search focus.
- **Location/Remote:** Change the ``geoId`` or remove ``f_WT=2`` in the job search URL for other locations or on-site jobs.
- **Experience Level:** Adjust ``f_E=1,2`` for other experience levels (see LinkedIn docs for codes).

Learnings & Best Practices
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Use broad, inclusive keywords to capture jobs for career changers and entry-level GenAI roles.
- LinkedIn rarely exposes direct emails or contact names; phone numbers are sometimes found.
- CAPTCHA/verification is common; manual solving is required.
- Use the CSV output for analysis in Excel or other tools.

Troubleshooting
^^^^^^^^^^^^^^^
- If you see ``[DEBUG] CAPTCHA or verification detected!``, solve the CAPTCHA in the browser window.
- If no jobs are found, try adjusting keywords, location, or experience filters.
- For language-specific jobs, add language keywords to the search or filter by description content.

Data Privacy
^^^^^^^^^^^^
- Do not share your LinkedIn credentials or scraped data publicly.
- Respect LinkedIn's terms of service and data privacy policies.

Making Output Files Untracked in Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To prevent ``genai_jobs_results.json`` and ``genai_jobs_results.csv`` from being tracked by git:

1. Add these lines to your ``.gitignore``::

   genai_jobs_results.json
   genai_jobs_results.csv

2. Remove them from git tracking (but keep them locally)::

   git rm --cached genai_jobs_results.json genai_jobs_results.csv
   git commit -m "Stop tracking job results files"

   Reference: https://www.geeksforgeeks.org/how-to-make-a-file-untracked-in-git/

Suggestions for Further Use
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Use the CSV for further analysis or visualization.
- Customize keywords and filters for other job types or locations.
- Consider converting documentation to Markdown for PyPI-friendliness (see https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/).

Installation
------------

.. code-block:: bash

   pip3 install --user linkedin_scraper

Version **2.0.0** and before is called ``linkedin_user_scraper`` and can be installed via ``pip3 install --user linkedin_user_scraper``

Setup
-----

First, you must set your chromedriver location by

.. code-block:: bash

   export CHROMEDRIVER=~/chromedriver


Usage
-----

To use it, just create the class.

Sample Usage
^^^^^^^^^^^^

.. code-block:: python

   from linkedin_scraper import Person, actions
   from selenium import webdriver
   driver = webdriver.Chrome()

   email = "some-email@email.address"
   password = "password123"
   actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
   person = Person("https://www.linkedin.com/in/joey-sham-aa2a50122", driver=driver)

**NOTE**\ : The account used to log-in should have it's language set English to make sure everything works as expected.

User Scraping
^^^^^^^^^^^^^

.. code-block:: python

   from linkedin_scraper import Person
   person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5")

Company Scraping
^^^^^^^^^^^^^^^^

.. code-block:: python

   from linkedin_scraper import Company
   company = Company("https://ca.linkedin.com/company/google")

Job Scraping
^^^^^^^^^^^^

.. code-block:: python

   from linkedin_scraper import JobSearch, actions
   from selenium import webdriver

   driver = webdriver.Chrome()
   email = "some-email@email.address"
   password = "password123"
   actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
   input("Press Enter")
   job = Job("https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3456898261", driver=driver, close_on_complete=False)

Job Search Scraping
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from linkedin_scraper import JobSearch, actions
   from selenium import webdriver

   driver = webdriver.Chrome()
   email = "some-email@email.address"
   password = "password123"
   actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
   input("Press Enter")
   job_search = JobSearch(driver=driver, close_on_complete=False, scrape=False)
   # job_search contains jobs from your logged in front page:
   # - job_search.recommended_jobs
   # - job_search.still_hiring
   # - job_search.more_jobs

   job_listings = job_search.search("Machine Learning Engineer") # returns the list of `Job` from the first page

Scraping sites where login is required first
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#. Run ``ipython`` or ``python``
#. In ``ipython``\ /\ ``python``\ , run the following code (you can modify it if you need to specify your driver)
#. 
   .. code-block:: python

      from linkedin_scraper import Person
      from selenium import webdriver
      driver = webdriver.Chrome()
      person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver = driver, scrape=False)

#. Login to Linkedin
#. [OPTIONAL] Logout of Linkedin
#. In the same ``ipython``\ /\ ``python`` code, run
   .. code-block:: python

      person.scrape()

The reason is that LinkedIn has recently blocked people from viewing certain profiles without having previously signed in. So by setting ``scrape=False``\ , it doesn't automatically scrape the profile, but Chrome will open the linkedin page anyways. You can login and logout, and the cookie will stay in the browser and it won't affect your profile views. Then when you run ``