from get_remotive_jobs import return_clean_json_data
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    response = return_clean_json_data()
    return {"message": response}, 200


if __name__ == "__main__":
    app.run(port=8080)
