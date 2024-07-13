from fetch_external_data import get_request
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    response = get_request("remotive", "https://remotive.com/api/remote-jobs")
    return {"message": response}, 200


if __name__ == "__main__":
    app.run(port=8080)
