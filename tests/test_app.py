import json

import pytest


class TestApp:
    def test_app_healthcheck(self, client):
        response = client.get("/healthcheck")
        resp = json.loads(response.data.decode("utf-8")).get("message")
        assert resp == "Wheather Airport by Tickets API is running"
        assert response.status_code == 200
