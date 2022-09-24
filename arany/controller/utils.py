from functools import wraps
from flask import request, current_app
from arany.model.dto import RequestBodyDTO
from werkzeug.exceptions import abort
from http import HTTPStatus


def validated_request_body(request_dto: RequestBodyDTO):
    def decorated_validated_request_body(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if request_dto.is_valid_json(request.get_json()):
                return view(*args, **kwargs)

            else:
                current_app.logger.error(
                    f"Invalid json body {request_dto.schema()} for {view.__name__}"
                )
                abort(
                    HTTPStatus.BAD_REQUEST,
                    description=f"Invalid json body expected a body in format: {request_dto.schema()}",
                )

        return wrapped_view

    return decorated_validated_request_body
