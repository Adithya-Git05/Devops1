import os
import time
import urllib.error
import urllib.request

EXPECTED_RESPONSE = "Hello, Jenkins Multi-Stage Pipeline!"
URL = os.environ.get("APP_URL", "http://127.0.0.1:5001/")


def main() -> None:
    deadline = time.monotonic() + 30
    last_error: urllib.error.URLError | None = None

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(URL, timeout=2) as response:
                body = response.read().decode("utf-8")
                if response.status != 200:
                    raise RuntimeError(f"Application returned HTTP {response.status}")
                if body != EXPECTED_RESPONSE:
                    raise AssertionError(f"Unexpected application response: {body!r}")
                print(f"HTTP {response.status}: {body}")
                return
        except urllib.error.URLError as error:
            last_error = error
            time.sleep(1)

    raise TimeoutError(f"Application did not become ready at {URL}: {last_error}")


if __name__ == "__main__":
    main()
