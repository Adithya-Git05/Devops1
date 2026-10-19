import unittest

from delivery_metrics import simulate_delivery


class DeliveryMetricsTests(unittest.TestCase):
    def test_simulated_delivery_metrics_are_consistent(self) -> None:
        metrics = simulate_delivery()

        self.assertEqual(
            metrics["total"],
            metrics["pending"] + metrics["on_the_way"] + metrics["delivered"],
        )
        self.assertGreaterEqual(metrics["pending"], 10)
        self.assertLessEqual(metrics["pending"], 20)
        self.assertGreaterEqual(metrics["delivery_time"], 15)
        self.assertLessEqual(metrics["delivery_time"], 45)


if __name__ == "__main__":
    unittest.main()
