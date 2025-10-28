from fastapi import APIRouter, status
from starlette.responses import FileResponse

from app.services.crud import build_countries_full_data, fetch_countries, fetch_country_by_name, \
    remove_country_by_name, fetch_status

router = APIRouter()

@router.post('/countries/refresh', status_code=status.HTTP_201_CREATED)
def refresh():

    return build_countries_full_data()

@router.get('/countries')
def get_countries(region: str = None, currency: str = None, sort: str = None):

    return fetch_countries(region, currency, sort)

@router.get("/countries/image")
def get_summary_image():
    image_path = "cache/summary.png"

    return FileResponse(image_path, media_type ="image/png")

@router.get('/countries/{name}')
def get_country_by_name(name: int):

    result = fetch_country_by_name(name)

    return result

@router.delete("/countries/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country_by_name(name: str):

    return remove_country_by_name(name)

@router.get("/status")
def get_status():
    return fetch_status()


