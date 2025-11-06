import os
import requests
import pandas as pd
import json


# ==========================================================
# CONFIGURATION
# ==========================================================

BASE_URL = "https://ffp.nl/wp-json/headline-livits/v1/search?gespecialiseerd_vermogensopbouw=vermogensopbouw"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output_ffp.csv")


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def fetch_json(url):
    """Fetch JSON data from the API"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Try to parse JSON safely
        try:
            data = response.json()
        except ValueError:
            data = json.loads(response.text)

        # If still string (double-encoded JSON)
        if isinstance(data, str):
            data = json.loads(data)

        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def extract_fields(planner):
    """Extract only required fields from each planner record"""

    def safe_strip(value):
        """Return empty string if None, else stripped string"""
        if value is None:
            return ""
        return str(value).strip()

    return {
        "Name": safe_strip(planner.get("naam_formeel_zonder_aanhef")),
        "Company": safe_strip(planner.get("bedrijfsnaam")),
        "Address": safe_strip(planner.get("adres")),
        "Postcode": safe_strip(planner.get("postcode")),
        "City": safe_strip(planner.get("plaats")),
        "Email": safe_strip(planner.get("email")),
        "Phone": safe_strip(planner.get("telefoon")),
        "Website": safe_strip(planner.get("web_adres")),
        "LinkedIn": safe_strip(planner.get("linkedIn")),
        "Profile_URL": f"https://ffp.nl/planner/{safe_strip(planner.get('url_key'))}",
        "Distance": safe_strip(planner.get("distance"))
    }

# ==========================================================
# MAIN SCRAPER LOGIC
# ==========================================================

def main():
    print("🚀 Starting FFP API scraper...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_planners = []
    total_pages = 9  # based on API info

    for page in range(1, total_pages + 1):
        print(f"📄 Fetching page {page} of {total_pages}...")

        url = f"{BASE_URL}&pageNumber={page}"
        data = fetch_json(url)

        if not data or "result" not in data:
            print(f"⚠️ Skipping page {page} (no data)")
            continue

        planners = data["result"]
        print(f"   → Got {len(planners)} planners")

        all_planners.extend(planners)

    print(f"\n✅ Total planners fetched: {len(all_planners)}")

    # Extract & clean
    cleaned_data = [extract_fields(p) for p in all_planners]

    # Convert to DataFrame
    df = pd.DataFrame(cleaned_data)

    # Export to CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"📁 Data successfully saved to: {OUTPUT_FILE}")

    print("\n📊 Preview:")
    print(df.head(5))

# ==========================================================
# RUN SCRIPT
# ==========================================================

if __name__ == "__main__":
    main()
