import random
import time

from prometheus_client import Gauge, Summary, start_http_server

total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge("pending_deliveries", "Number of pending deliveries")
on_the_way_deliveries = Gauge(
    "on_the_way_deliveries", "Number of deliveries on the way"
)
average_delivery_time = Summary(
    "average_delivery_time", "Average delivery time in seconds"
)


def simulate_delivery() -> dict[str, int | float]:
    pending = random.randint(10, 20)
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    delivery_time = random.uniform(15, 45)
    total = pending + on_the_way + delivered

    total_deliveries.set(total)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(delivery_time)

    return {
        "total": total,
        "pending": pending,
        "on_the_way": on_the_way,
        "delivered": delivered,
        "delivery_time": delivery_time,
    }


def main() -> None:
    print("Starting the metrics server on port 8000...")
    start_http_server(8000, addr="0.0.0.0")
    print("Metrics are available at http://localhost:8000/metrics")
    while True:
        metrics = simulate_delivery()
        print(
            f"total={metrics['total']} pending={metrics['pending']} "
            f"on_the_way={metrics['on_the_way']} "
            f"delivery_time={metrics['delivery_time']:.2f}s"
        )
        time.sleep(1)


if __name__ == "__main__":
    main()
