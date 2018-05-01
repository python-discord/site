from flask import jsonify

from pysite.base_route import APIView


class HealthCheckView(APIView):
    path = "/healthcheck"
    name = "api.healthcheck"

    def get(self):
        return jsonify({"status": "ok"})
