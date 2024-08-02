import sys
from flask import Flask, make_response, jsonify
from flask_cors import CORS, cross_origin
from fetch_external_data import return_clean_json_data
import utils.sql.sprocs as sprocs
import jobs_ingestion
from utils.data_cleaning.text_preprocessing import preprocess_text
from utils.sql.sql import MultipleRecordsFound, NoRecordsFound
from model import recommendation_engine_v001


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
        return make_response("Multiple choices", 300)
    except NoRecordsFound as e:
        print(f"Failed to fetch job {job_id}: {e}")
        return make_response("No content found", 404)


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


@cross_origin
@app.route("/api/recommendation_engine", methods=["GET"])
def get_recommendation():
    print("GET /api/recommendation_engine")

    # TODO This is hardwired just for testing
    #   Will need pass-through user_text, category_id, and requested quantity of results
    test_text = "I leverage expertise in molecular biology and computer science to provide program solutions and data insights to our molecular geneticists. My goal is to join in the transformation of precision medicine by delivering robust laboratory results."
    engine_results = recommendation_engine_v001.main(user_text=test_text, category_id=6, req_quant=15)

    # Gather job postings from engine_results
    response = sprocs.get_recommended_job_postings(engine_results, "Job.db")
    print("SUCCESS")
    return jsonify(response)

if __name__ == "__main__":
    # Set-up db at Flask initialization
    try:
        jobs_ingestion.main()
    except RuntimeError as e:
        err = f"ERROR: {e}"
        sys.exit()

    app.run(port=8080)
