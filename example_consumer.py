
import argparse
import json
import random
import urllib.error
import urllib.request


TARGET_SERVICE_NAME = "mattccs.test1"
DEFAULT_REGISTRY_URL = "http://127.0.0.1:12000"


def test_locate_service(name, registry_url=DEFAULT_REGISTRY_URL):
    url = f"{registry_url}/discover"
    req = urllib.request.Request(
        url=url,
        method="GET",
        headers={"Content-Type": "application/json"},
    )

    try:
        registry = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.read().decode())
        raise

    if (entry := registry.get(name)) is None:
        raise Exception("Service not found")

    return f"http://{entry['ip']}:{entry['port']}"


def test_health_check_service(name, url) -> True:
    url = f"{url}/health"
    req = urllib.request.Request(
        url=url,
        method="GET",
    )

    try:
        health = urllib.request.urlopen(req).read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise Exception(f"[!] Service unavailable at '{url}'!")

    if name != health:
        raise Exception(f"[!] Service mismatch on health check! Expected {name} but got {health}!")

    return health


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", type=str, default=TARGET_SERVICE_NAME)
    parser.add_argument("--registry", type=str, default=DEFAULT_REGISTRY_URL)
    return parser.parse_args()


def main():
    args = parse_args()
    print(target_url := test_locate_service(name=args.target, registry_url=args.registry))
    print(test_health_check_service(name=args.target, url=target_url))


if __name__ == "__main__":
    main()
