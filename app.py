from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(n: int) -> str:
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fact found."

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    try:
        number = int(request.args.get("number"))
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")

        return jsonify({
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": get_fun_fact(number)
        })
    except ValueError:
        return jsonify({"number": "invalid", "error": True}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

