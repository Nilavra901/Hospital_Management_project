import requests
import sys


def check(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code, r.text[:200]
    except Exception as e:
        return None, str(e)


def main():
    base = "http://127.0.0.1:8000"
    endpoints = ["/", "/health", "/patients"]
    all_ok = True
    for ep in endpoints:
        status, body = check(base + ep)
        if status is None:
            print(f"{ep}: ERROR -> {body}")
            all_ok = False
        else:
            print(f"{ep}: {status}")
    if not all_ok:
        sys.exit(2)
    print("Smoke test passed (server reachable).")


if __name__ == '__main__':
    main()
