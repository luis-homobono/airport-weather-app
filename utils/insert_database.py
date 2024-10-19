from typing import List, Dict
from http import HTTPStatus

import httpx
import pandas as pd
from flask import current_app
from flask_smorest import abort

from db import db
from .parrallel_process import apply_parallel
from models import AirportModel


def validate_airports(airports: List) -> bool:
    try:
        db_airports = db.session.query().with_entities(AirportModel.iata_code).all()
        db_data = [airport[0] for airport in db_airports]
        airports_ = [airport for airport in airports if airport not in db_data]
        return airports_
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, message="Internal server error")


def save_data(data: pd.DataFrame, airports: List) -> None:
    payloads = []
    airport_inserts = []
    key = current_app.config["WEATHER_API_KEY"]
    url = current_app.config["WEATHER_API_URL"]
    print(url)
    for airport in airports:
        if airport in data.origin_iata_code.unique():
            data_airport = data[data.origin_iata_code == airport].reset_index()
            name = data_airport.origin_name[0]
            latitude = float(data_airport.origin_latitude[0])
            longitude = float(data_airport.origin_longitude[0])
        else:
            data_airport = data[data.destination_iata_code == airport].reset_index()
            name = data_airport.destination_name[0]
            latitude = float(data_airport.destination_latitude[0])
            longitude = float(data_airport.destination_longitude[0])
        # print(f"Airport {name}: {airport}, Lat: {latitude}, Lon: {longitude}")
        airport_info = AirportModel(iata_code=airport, name=name, latitude=latitude,longitude=longitude)
        airport_inserts.append(airport_info)
        payloads.append({"latitude": latitude, "longitude": longitude, "airport_code": airport, "key": key, "url": url})
        # json_data = get_weather(latitude=latitude, longitude=longitude, airport_code=airport)
    responses = apply_parallel(func=get_weather, payloads=payloads)
    db.session.add_all(airport_inserts)
    db.session.commit()


def get_weather(airport_info: Dict) -> dict:
    
    params = {
        "q": f"{airport_info['latitude']},{airport_info['longitude']}",
        "days": 5,  # Forecasting
        "key": airport_info["key"],
        "url": airport_info["url"]
    }
    response = httpx.get(f"{airport_info['url']}", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {f"message": "Not get weather data for airport {airport_code}"}
