from flask import Blueprint, request, jsonify
from models import Pest_Detect, db
import base64

detectPest_bp = Blueprint('pest_detect', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all pest treatments
@detectPest_bp.route('/getDetectPests', methods=['GET'])
def get_detect_pests():
    try:
        # Query all pest treatments from the database
        detect_pests = Pest_Detect.query.all()

        # Prepare the response data
        result = []
        for dp in detect_pests:
            detect_pest_data = {
                "DetectId": dp.DetectId,
                "Username": dp.Username,
                "Pest_name": dp.Pest_name,
                "Image": dp.Image,
                "Detec_at": dp.Detect_at.strftime('%Y-%m-%d'),
            }
            
            if dp.Image:
                image_data = base64.b64encode(dp.Image).decode('utf-8')
                detect_pest_data["Image"] = image_data

            result.append(detect_pest_data)

        return create_response(data=result, message="Detect pests fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch detect pests", status=500)
    
# Get a specific pest treatment by ID (with image as BLOB)
@detectPest_bp.route('/getDetectPest/<int:detect_id>', methods=['GET'])
def get_detect_pest(detect_id):
    try:
        # Query pest treatment by ID
        detect_pest = Pest_Detect.query.get_or_404(detect_id)

        # Prepare the pest treatment data
        detect_pest_data = {
            "DetectId": detect_pest.DetectId,
            "Username": detect_pest.Username,
            "Pest_name": detect_pest.Pest_name,
            "Image": detect_pest.Image,
            "Detec_at": detect_pest.Detect_at.strftime('%Y-%m-%d'),
        }

        return create_response(data=detect_pest_data, message="Detect pest fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch detect pest", status=500)