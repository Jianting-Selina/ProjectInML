from flask import Flask, request, jsonify
import uuid
import os
import random

app = Flask(__name__)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simulated database
database = {
    "images": {},
    "reports": {}
}

# 1. Upload MRI Image API
@app.route("/BrainTumorAPI/upload", methods=["POST"])
def upload_image():
    patient_id = request.form.get("patient_id")
    image = request.files.get("image")

    if not patient_id or not image:
        return jsonify({"error": "Missing patient_id or image"}), 400

    image_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{image_id}_{image.filename}")
    
    image.save(file_path)

    database["images"][image_id] = {"patient_id": patient_id, "file_path": file_path}
    
    return jsonify({"status": "uploaded", "image_id": image_id}), 200

# 2. Run Tumor Detection API
@app.route("/BrainTumorAPI/detect", methods=["POST"])
def detect_tumor():
    data = request.get_json()
    image_id = data.get("image_id")

    if not image_id or image_id not in database["images"]:
        return jsonify({"error": "Image not found"}), 404

    # Mock tumor detection logic
    tumor_types = ["Glioblastoma", "Meningioma", "No Tumor Detected"]
    detected_tumor = random.choice(tumor_types)
    confidence = round(random.uniform(0.85, 0.99), 2)

    # Store report
    report_id = str(uuid.uuid4())
    database["reports"][report_id] = {
        "image_id": image_id,
        "tumor_type": detected_tumor,
        "confidence": confidence,
        "patient_id": database["images"][image_id]["patient_id"]
    }

    return jsonify({"status": "completed", "tumor_type": detected_tumor, "confidence": confidence, "report_id": report_id}), 200

# 3. Retrieve Tumor Detection Report API
@app.route("/BrainTumorAPI/report/<report_id>", methods=["GET"])
def get_report(report_id):
    if report_id not in database["reports"]:
        return jsonify({"error": "Report not found"}), 404

    report = database["reports"][report_id]
    recommendations = "Refer to oncology specialist" if report["tumor_type"] != "No Tumor Detected" else "No further action needed"
    
    return jsonify({
        "report_id": report_id,
        "patient_id": report["patient_id"],
        "tumor_type": report["tumor_type"],
        "confidence": report["confidence"],
        "recommendations": recommendations
    }), 200
# 4. Request Patient Consent
@app.route('/MeshNetAPI/consent/<string:patient_id>', methods=['POST'])
def request_consent(patient_id):
    """Request and store patient consent for AI-based diagnosis."""
    data = request.get_json()
    
    if not data or 'consent' not in data:
        return jsonify({"error": "Missing consent parameter"}), 400
    
    # Store the patient's consent
    patient_consents[patient_id] = data['consent']

    return jsonify({
        "message": "Consent recorded successfully",
        "patient_id": patient_id,
        "consent_given": data['consent']
    }), 200
if __name__ == "__main__":
    app.run(debug=True)
