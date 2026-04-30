from flask import Flask, request

app = Flask(__name__)

latest_alert = "No alerts"

@app.route("/alert", methods=["POST"])
def alert():
    global latest_alert
    data = request.json
    latest_alert = data.get("message", "Alert")
    print("ALERT RECEIVED:", latest_alert)
    return {"status": "ok"}

@app.route("/")
def home():
    return f"<h1>{latest_alert}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)