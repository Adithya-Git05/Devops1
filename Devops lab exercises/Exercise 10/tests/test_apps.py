import unittest

import product_catalog
import shopping_cart


class ProductCatalogTests(unittest.TestCase):
    def test_products_endpoint_returns_catalog(self) -> None:
        response = product_catalog.app.test_client().get("/products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)
        self.assertEqual(response.get_json()[0]["name"], "Laptop")


class ShoppingCartTests(unittest.TestCase):
    def setUp(self) -> None:
        shopping_cart.cart.clear()
        self.client = shopping_cart.app.test_client()

    def test_cart_can_be_read_and_updated(self) -> None:
        self.assertEqual(self.client.get("/cart").get_json(), [])

        response = self.client.post(
            "/cart",
            json={"id": 1, "name": "Laptop", "quantity": 1},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()[0]["name"], "Laptop")

    def test_cart_rejects_non_object_json(self) -> None:
        response = self.client.post("/cart", json=["not", "an", "item"])

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
