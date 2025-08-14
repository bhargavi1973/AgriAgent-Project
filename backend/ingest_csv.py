"""
Bulk-ingests AgriAgent vector store using a CSV list of (district, crop) pairs.
"""

import csv
import time
import os
from data_fetcher import get_weather_data, get_market_data, get_soil_health
from rag_pipeline import upsert_agri_facts

CSV_PATH = os.path.join(os.path.dirname(__file__), "ingest_list.csv")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"❌ CSV file not found: {CSV_PATH}")
        print("Please create 'ingest_list.csv' with 'district,crop' columns.")
        return

    total_facts = 0
    total_rows = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            district = row.get("district", "").strip()
            crop = row.get("crop", "").strip()
            if not district or not crop:
                continue

            print(f"📥 Fetching for {district} - {crop} ...")
            weather = get_weather_data(district)
            market = get_market_data(crop)
            soil = get_soil_health(district)

            count = upsert_agri_facts(district, crop, weather, market, soil)
            total_facts += count
            total_rows += 1
            time.sleep(0.5)  # avoid hammering APIs

    print(f"\n✅ Ingestion complete.")
    print(f"   Lcd backendoaded {total_rows} district-crop pairs.")
    print(f"   Added {total_facts} fact chunks to the vector store.")

if __name__ == "__main__":
    main()
