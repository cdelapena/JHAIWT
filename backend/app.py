from flask import Flask, make_response, jsonify
from fetch_external_data import return_clean_json_data
from text_preprocessing import preprocess_text
import sprocs
from utils.sql.sql import MultipleRecordsFound


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    response = return_clean_json_data(
        "remotive", "https://remotive.com/api/remote-jobs"
    )
    response = preprocess_text(response)
    return {"message": response}, 200


@app.route("/api/job", methods=["GET"])
def get_all():
    print("GET api/job")
    response = sprocs.get_all_job_postings("Job.db")
    print("SUCCESS")
    return jsonify(response)


@app.route("/api/job/<job_id>", methods=["GET"])
def get_job(job_id):
    print(f"GET api/job/{job_id}")
    try:
        response = sprocs.get_job_posting(job_id, "Job.db")
        print("SUCCESS")
        return jsonify(response)
    except MultipleRecordsFound as e:
        print(f"Failed to fetch job {job_id}: {e}")
        return make_response("No content found", 409)


if __name__ == "__main__":
    app.run(port=8080)
