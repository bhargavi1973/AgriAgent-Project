"""
Pre-loads AgriAgent vector store with facts for multiple (district, crop) pairs.
Run this once before the demo to ensure the RAG has rich context.
"""

import time
from data_fetcher import get_weather_data, get_market_data, get_soil_health
from rag_pipeline import upsert_agri_facts

# Define the district-crop pairs you want to pre-load
DISTRICTS = ["Bareilly", "Pune", "Lucknow", "Ahmedabad"]
CROPS = ["wheat", "rice", "cotton"]

def main():
    total_facts = 0
    for district in DISTRICTS:
        for crop in CROPS:
            print(f"Fetching data for {district} - {crop} ...")
            weather = get_weather_data(district)
            market = get_market_data(crop)
            soil = get_soil_health(district)

            count = upsert_agri_facts(district, crop, weather, market, soil)
            total_facts += count
            time.sleep(0.5)  # polite delay for API calls

    print(f"\n✅ Ingestion complete. {total_facts} fact chunks added to the vector store.")

if __name__ == "__main__":
    main()
