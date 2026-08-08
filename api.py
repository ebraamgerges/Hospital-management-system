from flask import Flask, jsonify, request
from flask_cors import CORS

from main1 import (
    FileStorage,
    find_existing_patient,
    load_doctors_from_csv
)

app = Flask(__name__)
CORS(app)

storage = FileStorage()


@app.get("/api/patients/<patient_id>")
def get_patient(patient_id):

    patient = find_existing_patient(patient_id)

    if patient is None:
        return jsonify({
            "success": False,
            "message": "Patient not found"
        }), 404

    return jsonify({
        "success": True,
        "patient": patient
    })


@app.get("/api/patients/<patient_id>/history")
def get_patient_history(patient_id):

    reports_file = "reports_data.json"

    try:
        reports = storage.load_data(reports_file)
    except Exception:
        reports = []

    history = [
        report
        for report in reports
        if str(report.get("patient_id")) == str(patient_id)
    ]

    return jsonify({
        "success": True,
        "history": history
    })


@app.get("/api/doctors")
def get_doctors():

    doctors = load_doctors_from_csv("doctors_data.csv")

    return jsonify({
        "success": True,
        "doctors": [
            doctor.to_dict()
            for doctor in doctors
        ]
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )