import json
import time
import urllib.error
import urllib.request

METRICS_URL = "http://127.0.0.1:8000/metrics"
PROMETHEUS_URL = "http://127.0.0.1:9090"
GRAFANA_URL = "http://127.0.0.1:3000"


def get_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=3) as response:
        return response.read().decode("utf-8")


def wait_for(description: str, check, timeout: float = 60) -> None:
    deadline = time.monotonic() + timeout
    last_error: urllib.error.URLError | None = None

    while time.monotonic() < deadline:
        try:
            if check():
                print(f"Verified: {description}")
                return
        except urllib.error.URLError as error:
            last_error = error
        time.sleep(2)

    raise TimeoutError(f"Timed out waiting for {description}: {last_error}")


def metrics_ready() -> bool:
    metrics = get_text(METRICS_URL)
    return all(
        name in metrics
        for name in (
            "total_deliveries ",
            "pending_deliveries ",
            "on_the_way_deliveries ",
            "average_delivery_time_sum ",
        )
    )


def delivery_target_ready() -> bool:
    targets = json.loads(get_text(f"{PROMETHEUS_URL}/api/v1/targets"))
    return any(
        target.get("labels", {}).get("job") == "delivery_service"
        and target.get("health") == "up"
        for target in targets["data"]["activeTargets"]
    )


def rules_loaded() -> bool:
    result = json.loads(get_text(f"{PROMETHEUS_URL}/api/v1/rules?type=alert"))
    names = {
        rule["name"]
        for group in result["data"]["groups"]
        for rule in group["rules"]
    }
    return {
        "HighPendingDeliveries",
        "HighAverageDeliveryTime",
    }.issubset(names)


def pending_alert_firing() -> bool:
    result = json.loads(get_text(f"{PROMETHEUS_URL}/api/v1/alerts"))
    return any(
        alert["labels"].get("alertname") == "HighPendingDeliveries"
        and alert.get("state") == "firing"
        for alert in result["data"]["alerts"]
    )


def grafana_ready() -> bool:
    health = json.loads(get_text(f"{GRAFANA_URL}/api/health"))
    return health.get("database") == "ok"


def main() -> None:
    wait_for("delivery metrics endpoint", metrics_ready)
    wait_for("Prometheus delivery target is up", delivery_target_ready)
    wait_for("both Prometheus alert rules are loaded", rules_loaded)
    wait_for("high-pending-deliveries alert is firing", pending_alert_firing)
    wait_for("Grafana is healthy", grafana_ready)


if __name__ == "__main__":
    main()
