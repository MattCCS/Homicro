
import argparse
import json
import random
import urllib.error
import urllib.request

from flask import Flask, request


SERVICE_NAME = "mattccs.test1"
DEFAULT_REGISTRY_URL = "http://127.0.0.1:12000"


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return SERVICE_NAME


def self_register(name, port, registry_url=DEFAULT_REGISTRY_URL):
    url = f"{registry_url}/register"
    data = {
        "name": name,
        "port": port,
        "expire": 0,
    }

    req = urllib.request.Request(
        url=url,
        method="PUT",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data).encode("utf-8"),
    )

    try:
        print(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as exc:
        print(exc.read().decode())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=None)
    parser.add_argument("--registry", type=str, default=DEFAULT_REGISTRY_URL)
    return parser.parse_args()


def main():
    args = parse_args()
    port = args.port or random.randint(1025, 65535)
    self_register(name=SERVICE_NAME, port=port, registry_url=args.registry)
    app.run(host="127.0.0.1", threaded=True, port=port)


if __name__ == "__main__":
    main()
