from flask import jsonify


class ErrorHandler:
    @staticmethod
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @staticmethod
    def invalid_json_body(e):
        return jsonify(error=str(e)), 400
