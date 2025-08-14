# backend/data_fetcher.py
import os
import requests

# Data.gov.in API key from environment
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")

# ---------- LIVE DATA FUNCTIONS ----------
def get_weather_data(location: str):
    """
    Fetch 7-day district-level weather forecast from data.gov.in (IMD dataset)
    """
    try:
        url = "https://api.data.gov.in/resource/65f3d1a2-43db-4a2a-a1b3-fc5f45a7b5d2"  # Replace with correct IMD dataset ID
        params = {
            "api-key": DATA_GOV_API_KEY,
            "format": "json",
            "filters[district]": location
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        if data.get("records"):
            forecast = data["records"][0].get("forecast", "No forecast available")
            return {"forecast": forecast, "risk": "Check details"}
    except Exception as e:
        print(f"[Weather API Error]: {e}")

    return get_weather_data_mock(location)


def get_market_data(crop: str):
    """
    Fetch mandi price data from Agmarknet via data.gov.in
    """
    try:
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"  # Replace with Agmarknet dataset ID
        params = {
            "api-key": DATA_GOV_API_KEY,
            "format": "json",
            "filters[commodity]": crop
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        if data.get("records"):
            latest = data["records"][0]
            return {
                "latest_price": latest.get("modal_price", "N/A"),
                "trend": "Stable"
            }
    except Exception as e:
        print(f"[Market API Error]: {e}")

    return get_market_data_mock(crop)


def get_soil_health(location: str):
    """
    Fetch soil health card data from data.gov.in
    """
    try:
        url = "https://api.data.gov.in/resource/3f89f5a2-55ae-4d0e-94e0-63a64dfd28ba"  # Replace with correct SHC dataset ID
        params = {
            "api-key": DATA_GOV_API_KEY,
            "format": "json",
            "filters[district_name]": location
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        if data.get("records"):
            record = data["records"][0]
            return {
                "status": f"N: {record.get('available_n', 'NA')}, P: {record.get('available_p', 'NA')}, K: {record.get('available_k', 'NA')}",
                "recommendation": "Apply recommended nutrients as per SHC"
            }
    except Exception as e:
        print(f"[SHC API Error]: {e}")

    return get_soil_health_mock(location)


# ---------- MOCK DATA FUNCTIONS ----------
def get_weather_data_mock(location: str):
    return {"forecast": "No rainfall next 7 days", "risk": "Low moisture"}

def get_market_data_mock(crop: str):
    return {"latest_price": "₹2,100/quintal", "trend": "Prices stable"}

def get_soil_health_mock(location: str):
    return {"status": "Low nitrogen", "recommendation": "Apply urea"}
