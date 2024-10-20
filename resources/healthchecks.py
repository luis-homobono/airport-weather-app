from http import HTTPStatus

from flask import jsonify
from flask_smorest import Blueprint, abort

from cache import redis_client

blp = Blueprint("Healthchecks operations", __name__, description="Endpoints for healthchecks services")

@blp.route("/healthcheck")
@blp.response(HTTPStatus.OK)
def healthcheck():
    return jsonify({"message": "Wheather Airport by Tickets API is running"})

@blp.route("/redis-healtcheck")
@blp.response(HTTPStatus.OK)
def redis_healtcheck():
    try:
        cached_response = redis_client.get('redis_test')
        if cached_response:
            return jsonify({"message": cached_response.decode("utf-8")})
        
        redis_test = "Redis service is running"
        redis_client.set("redis_test", redis_test, ex=5)  # Cached for 5 seconds

        return jsonify({"message": "Redis service has cached a value"})
    except:
        abort(HTTPStatus.BAD_REQUEST, message="Redis service connection error")

@blp.route("/redis-clener/<string:key>", methods=["DELETE"])
@blp.response(HTTPStatus.OK)
def clean_redis(key):
    try:
        redis_client.delete(key)
        return jsonify({"message": "Redis service has deleted a value"})
    except:
        abort(HTTPStatus.BAD_REQUEST, message="Redis service connection error")
