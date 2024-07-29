from flask import Flask, make_response, jsonify, request
from flask_cors import CORS, cross_origin
from fetch_external_data import return_clean_json_data
import sprocs
from utils.data_cleaning.text_preprocessing import preprocess_text
from utils.sql.sql import MultipleRecordsFound


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@cross_origin()
@app.route("/", methods=["GET"])
def home():
    response = return_clean_json_data(
        "remotive", "https://remotive.com/api/remote-jobs"
    )
    response = preprocess_text(response)
    return {"message": response}, 200


@cross_origin()
@app.route("/api/job", methods=["GET"])
def get_all_jobs():
    print("GET /api/job")
    response = sprocs.get_all_job_postings("Job.db")
    print("SUCCESS")
    return jsonify(response)


@cross_origin()
@app.route("/api/job/results", methods=["POST"])
def get_filtered_jobs():
    data = request.get_json()
    print(f"POST /api/job/results with data: {data}")
    # Implement logic to filter jobs based on received data
    # response = sprocs.get_filtered_job_postings("Job.db", data)
    response = {"message": "Filtered jobs based on relevant skills"}
    print("SUCCESS")
    return jsonify(response)


@cross_origin()
@app.route("/api/job/results/<int:number>", methods=["GET", "POST"])
def get_some_jobs(number):
    print(f"GET /api/job/results/{number}")
    response = sprocs.get_some_job_postings("Job.db", number)
    print("SUCCESS")
    return jsonify(response)


@cross_origin()
@app.route("/api/job/<job_id>", methods=["GET"])
def get_job(job_id):
    print(f"GET /api/job/{job_id}")
    try:
        response = sprocs.get_job_posting(job_id, "Job.db")
        print("SUCCESS")
        return jsonify(response)
    except MultipleRecordsFound as e:
        print(f"Failed to fetch job {job_id}: {e}")
        return make_response("No content found", 409)


@cross_origin()
@app.route("/api/tag", methods=["GET"])
def get_all_tags():
    print("GET /api/tag")
    response = sprocs.get_tags("Job.db")
    print("SUCCESS")
    return jsonify(response)


@cross_origin()
@app.route("/api/category", methods=["GET"])
def get_all_categories():
    print("GET /api/category")
    response = sprocs.get_categories("Job.db")
    print("SUCCESS")
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8080)
