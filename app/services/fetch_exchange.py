import requests
from fastapi import HTTPException


def fetch_country_data():
    try:
        response = requests.get("https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies")
        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="External API timed out")

    except requests.ConnectionError:
        raise HTTPException(status_code=502, detail="Failed to connect to external API")

    except requests.HTTPError:
        raise HTTPException(status_code=response.status_code, detail="External API returned an error")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


def fetch_exchange_rates():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="External API timed out")

    except requests.ConnectionError:
        raise HTTPException(status_code=502, detail="Failed to connect to external API")

    except requests.HTTPError:
        raise HTTPException(status_code=response.status_code, detail="External API returned an error")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


