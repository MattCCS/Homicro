
import json

from flask import Flask, request
from pydantic.error_wrappers import ValidationError

import commands
import models
from commands import ActionNotAllowedException


app = Flask(__name__)


@app.route("/register", methods=["PUT"])
def register():
    source_ip = request.environ["REMOTE_ADDR"]

    try:
        data = models.SelfRegisterRequest(**request.json)
    except ValidationError as exc:
        return (str(exc), 400)

    try:
        result = commands.register(
            source_ip=source_ip,
            name=data.name,
            port=data.port,
            expire=data.expire,
        )
    except ActionNotAllowedException as exc:
        return (str(exc), 403)

    return str(result)


@app.route("/discover", methods=["GET"])
def discover():
    results = commands.discover()
    return json.dumps(results)
