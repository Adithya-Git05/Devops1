import time
import urllib.error
import urllib.request
from pathlib import Path

import docker

PROFILE = "my-apparmor-profile"
IMAGE = "flask-apparmor"
ROOT = Path(__file__).resolve().parent


def wait_for_application(url: str, timeout: float = 20) -> str:
    deadline = time.monotonic() + timeout
    last_error: urllib.error.URLError | None = None

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                body = response.read().decode("utf-8")
                if response.status != 200:
                    raise RuntimeError(f"Flask returned HTTP {response.status}")
                return body
        except urllib.error.URLError as error:
            last_error = error
            time.sleep(0.5)

    raise TimeoutError(f"Flask did not become ready at {url}: {last_error}")


def main() -> None:
    client = docker.from_env()
    client.images.build(path=str(ROOT), tag=IMAGE)
    container = client.containers.run(
        IMAGE,
        ports={"5000/tcp": ("127.0.0.1", 5000)},
        security_opt=[f"apparmor={PROFILE}"],
        detach=True,
    )

    try:
        info = client.api.inspect_container(container.id)
        apparmor_profile = info.get("AppArmorProfile", "")
        security_options = info["HostConfig"].get("SecurityOpt") or []
        if f"apparmor={PROFILE}" not in security_options:
            raise RuntimeError(f"Container security options do not include {PROFILE}")
        if apparmor_profile != PROFILE:
            raise RuntimeError(
                f"Expected active AppArmor profile {PROFILE!r}, "
                f"got {apparmor_profile!r}"
            )

        body = wait_for_application("http://127.0.0.1:5000/")
        print(f"Active AppArmor profile: {apparmor_profile}")
        print(f"Flask returned HTTP 200: {body}")
    finally:
        container.stop()
        container.remove()


if __name__ == "__main__":
    main()
