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
    "reports": {},
    "segmentations": {},
    "progressions": {}
}

# USE CASE 1
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

## USE CASE 2
# 5. Perform image segmentation to detect and highlight the tumor region.
@app.route("/BrainTumorAPI/segment", methods=["POST"])
def segment_tumor():
    data = request.get_json()
    image_id = data.get("image_id")

    if not image_id:
        return jsonify({"error": "Image ID is required"}), 400
    if image_id not in database["images"]:
        return jsonify({"error": "Image not found"}), 404

    # Simulated segmentation process
    segmentation_id = str(uuid.uuid4())
    tumor_detected = random.choice([True, False])
    confidence = round(random.uniform(0.85, 0.99), 2) if tumor_detected else None
    segmentation_mask_url = f"http://srv/BrainTumorAPI/masks/{segmentation_id}.png" if tumor_detected else None
    tumor_region = {"x": random.randint(100, 200), "y": random.randint(100, 200), "width": 80, "height": 90} if tumor_detected else None

    database["segmentations"][segmentation_id] = {
        "image_id": image_id,
        "patient_id": database["images"][image_id]["patient_id"],
        "tumor_detected": tumor_detected,
        "confidence": confidence,
        "segmentation_mask_url": segmentation_mask_url,
        "tumor_region_coordinates": tumor_region
    }
    
    return jsonify({
        "segmentation_id": segmentation_id,
        "image_id": image_id,
        "patient_id": database["images"][image_id]["patient_id"],
        "tumor_detected": tumor_detected,
        "confidence": confidence,
        "segmentation_mask_url": segmentation_mask_url,
        "tumor_region_coordinates": tumor_region
    }), 200 if tumor_detected else 204

#6 Analyze tumor progression by comparing past and recent MRI scans
@app.route("/BrainTumorAPI/progression", methods=["POST"])
def analyze_progression():
    data = request.get_json()
    patient_id = data.get("patient_id")
    latest_image_id = data.get("latest_image_id")
    previous_image_id = data.get("previous_image_id")

    if not patient_id or not latest_image_id or not previous_image_id:
        return jsonify({"error": "Both image IDs are required"}), 400
    if latest_image_id not in database["images"] or previous_image_id not in database["images"]:
        return jsonify({"error": "MRI scan not found for comparison"}), 404

    # Simulated tumor progression analysis
    progression_status = random.choice(["increased", "stable", "decreased"])
    size_difference = f"{random.randint(5, 20)}% {progression_status}" if progression_status != "stable" else "No significant change"
    confidence = round(random.uniform(0.85, 0.99), 2)

    return jsonify({
        "patient_id": patient_id,
        "latest_image_id": latest_image_id,
        "previous_image_id": previous_image_id,
        "progression_status": progression_status,
        "size_difference": size_difference,
        "confidence": confidence
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
