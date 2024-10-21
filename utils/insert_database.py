from http import HTTPStatus
from typing import List, Dict

import httpx
import redis
import pandas as pd
from flask import current_app
from flask_smorest import abort

from db import db

from models import AirportModel, FlightModel
from .parrallel_process import apply_parallel
from .cache_handler import cache_data, persist_data


def validate_airports(airports: List) -> bool:
    try:
        db_airports = db.session.query().with_entities(AirportModel.iata_code).all()
        db_data = [airport[0] for airport in db_airports]
        airports_ = [airport for airport in airports if airport not in db_data]
        return airports_
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, message="Internal server error")


def save_data(data: pd.DataFrame, airports: List[str]) -> List[Dict]:
    payloads = []
    airport_inserts = []
    key = current_app.config["WEATHER_API_KEY"]
    url = current_app.config["WEATHER_API_URL"]
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
        airport_info = AirportModel(
            iata_code=airport, name=name, latitude=latitude, longitude=longitude
        )
        airport_inserts.append(airport_info)
        payloads.append(
            {
                "latitude": latitude,
                "longitude": longitude,
                "airport_code": airport,
                "key": key,
                "url": url,
            }
        )
    responses = apply_parallel(func=get_weather, payloads=payloads)
    try:
        cache_data(responses=responses[0])
    except:
        persist_data(responses=responses[0])  # Check how to get nested list

    db.session.add_all(airport_inserts)
    db.session.commit()
    return responses[0]


def get_weather(airport_info: Dict) -> dict:
    params = {
        "q": f"{airport_info['latitude']},{airport_info['longitude']}",
        # "days": 5,  # Forecasting
        "key": airport_info["key"],
    }
    response = httpx.get(f"{airport_info['url']}", params=params)
    if response.status_code == 200:
        data = response.json()
        data["code"] = airport_info["airport_code"]
        return data
    else:
        return {f"message": "Not get weather data for airport {airport_code}"}


def save_fligths(tickets_data: pd.DataFrame) -> None:
    flight_inserts = []
    for index, flight_row in tickets_data.iterrows():
        flight = FlightModel(
            airline=flight_row.airline,
            flight_num=flight_row.flight_num,
            origin_iata_code=flight_row.origin_iata_code,
            destination_iata_code=flight_row.destination_iata_code,
        )
        flight_inserts.append(flight)
    db.session.add_all(flight_inserts)
    db.session.commit()
