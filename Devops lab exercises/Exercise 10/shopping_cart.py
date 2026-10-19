from flask import Flask, abort, jsonify, request

app = Flask(__name__)
cart = []


@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)


@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.get_json(silent=True)
    if not isinstance(item, dict):
        abort(400, description="Request body must be a JSON object")
    cart.append(item)
    return jsonify(cart), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
