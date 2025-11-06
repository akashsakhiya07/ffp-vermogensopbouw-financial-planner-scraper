# 🧠 FFP Vermogensopbouw Financial Planner Scraper

This project is a **real-world web scraping task** inspired by an Upwork job post.
The goal was to extract all contact information (emails, phone numbers, addresses, etc.)
of financial planners categorized under **"Vermogensopbouw"** from the official  
[FFP website](https://ffp.nl/vind-een-planner/).

---

## 🚀 Project Overview

The official FFP website contains a directory of certified financial planners.  
The task was to scrape all **169 contacts** under the "Vermogensopbouw" category.

However, after analyzing the website, we discovered that the data is actually loaded  
via an internal **WordPress REST API** endpoint. This allowed us to build a fast,  
clean, and production-ready scraper without browser automation.

**Final API used:**

https://ffp.nl/wp-json/headline-livits/v1/search?gespecialiseerd_vermogensopbouw=vermogensopbouw


This API returned real-time JSON data containing planner details such as:
- Name  
- Company  
- Address  
- Postal Code  
- City  
- Email  
- Phone  
- Website  
- LinkedIn  
- Profile URL  
- Distance  

At the time of scraping, the live API returned **180 planners** (slightly higher than 169 due to updates in their database).


---

## 🧰 How It Works

1. The script directly connects to FFP's JSON API using Python’s `requests` library.  
2. It loops through all 9 pages of API data (`pageNumber=1 to 9`).  
3. For each record, it extracts the necessary fields and handles missing values safely.  
4. The cleaned data is then stored in a **CSV file (`data/output_ffp.csv`)** using `pandas`.

---

## 🧾 Output Example (CSV)

| Name | Company | City | Email | Phone | Website |
|------|----------|------|--------|--------|----------|
| G. van der Woude CFP® | CNV | Utrecht | g.vanderwoude@cnv.nl | 0614956217 | www.cnv.nl |
| R.F.A. van Wolde CFP® | Van Wolde Financieel Advies | Utrecht | rolf@vanwolde.com | (030) 275 90 80 | vanwolde.com |

---

## 🧠 Key Learnings

- How to inspect **Network/XHR** requests in Chrome DevTools  
- How to identify and use hidden API endpoints instead of scraping HTML  
- Safe handling of `NoneType` data in JSON fields  
- Building a **modular scraper** with pagination and clean output  
- Professional project documentation for portfolio presentation  

---

## 🪄 Possible Future Improvements

- Integrate **Playwright** to simulate browser-based filtering (UI automation).  
- Store data in a database (e.g., SQLite or PostgreSQL).  
- Add logging, retry logic, and auto-scheduling (cron job).  

---