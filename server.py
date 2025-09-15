from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "https://open.er-api.com/v6/latest/"

@app.route("/")
def home():
    return render_template("index.html")   # serve your frontend

@app.route("/convert", methods=["GET"])
def convert_currency():
    try:
        amount = float(request.args.get("amount"))
        from_currency = request.args.get("from")
        to_currency = request.args.get("to")

        if not from_currency or not to_currency:
            return jsonify({"error": "Missing currency parameters"}), 400
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400

        response = requests.get(API_URL + from_currency)
        data = response.json()

        if data.get("result") != "success":
            return jsonify({"error": "API error"}), 500

        rates = data.get("rates", {})
        if to_currency not in rates:
            return jsonify({"error": f"Currency {to_currency} not available"}), 400

        converted_amount = amount * rates[to_currency]

        return jsonify({
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "converted": round(converted_amount, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
