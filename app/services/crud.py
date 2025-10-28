import json
import random
from datetime import timezone
from zoneinfo import ZoneInfo

from app.repository.repository import upsert, filter, read_by_name, delete_by_name, compute_status_fields, \
    compute_summary_data
from app.services.fetch_exchange import fetch_country_data, fetch_exchange_rates
from app.services.generate_image import generate_country_summary_image


def build_countries_full_data(countries=None, rates=None):
    countries = fetch_country_data()
    rates = fetch_exchange_rates()

    countries_full = []

    compute_gdp = lambda pop, rand, ex_rate: (pop * rand / ex_rate) if ex_rate else None

    for record in countries:

        rand_int = random.randint(1000, 2000)
        population = record.get("population")
        currencies = record.get("currencies")

        if not currencies:
            currency_code = None
            rate = None
            estimated_gdp = 0
        else:
            currency_code = currencies[0].get("code")
            rate = rates.get("rates").get(currency_code)
            estimated_gdp = compute_gdp(population, rand_int, rate)


        country = {
            'name': record.get("name"),
            'capital': record.get("capital"),
            'region': record.get("region"),
            'population': population,
            "currency_code": currency_code,
            "exchange_rate": rate,
            "estimated_gdp": estimated_gdp,
            'flag_url': record.get("flag")
        }

        countries_full.append(country)

    upsert(countries_full)

    cache_summary_image()

    return {"message": f"{len(countries_full)} countries saved successfully."}


def fetch_countries(region = None, currency_code = None, sort = None):
    if sort:
        sort_column, order_string = sort.split('_')
        order = True if order_string.lower() == 'asc' else False
    else:
        sort_column, order = None, None

    results = filter(region=region, currency_code=currency_code, order_by=sort_column, ascending=order)

    return results


def fetch_country_by_name(name: str):

    return read_by_name(name)

def remove_country_by_name(name: str):

    return delete_by_name(name)

def fetch_status():
    last_refreshed_at, total = compute_status_fields()
    last_refreshed_at = last_refreshed_at.astimezone(timezone.utc).isoformat()

    return {
        "total_countries": total,
        "last_refreshed_at": last_refreshed_at
    }


def fetch_summary_data():
    result = compute_summary_data()
    last_refreshed_at, total, top_5 = result#[result.get(k) for k in ['last_refreshed_at', 'total', 'top_5']]

    # top_5 = [topfor i in top_5]
    last_refreshed_at = last_refreshed_at.astimezone(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M:%S %Z")

    summary_data = {
        "total_countries": total,
        "last_refreshed_at": last_refreshed_at,
        "top_5": top_5
    }

    return summary_data


def cache_summary_image():
    generate_country_summary_image(fetch_summary_data())

    return

