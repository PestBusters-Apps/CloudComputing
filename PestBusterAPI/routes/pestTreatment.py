from flask import Blueprint, request, jsonify
from models import Pest_Treatment, db
import base64

pest_treatment_bp = Blueprint('pest_treatment', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all pest treatments
@pest_treatment_bp.route('/getPestTreatments', methods=['GET'])
def get_pest_treatments():
    try:
        # Query all pest treatments from the database
        pest_treatments = Pest_Treatment.query.all()

        # Prepare the response data
        result = []
        for pt in pest_treatments:
            pest_treatment_data = {
                "PestId": pt.PestId,
                "Pest_name": pt.Pest_name,
                "Treat_material": pt.Treat_material,
                "Treatment": pt.Treatment,
                "Created_at": pt.Created_at.strftime('%Y-%m-%d'),
            }
            
            if pt.Image:
                image_data = base64.b64encode(pt.Image).decode('utf-8')
                pest_treatment_data["Image"] = image_data

            result.append(pest_treatment_data)

        return create_response(data=result, message="Pest treatments fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch pest treatments", status=500)
    
# Get a specific pest treatment by ID (with image as BLOB)
@pest_treatment_bp.route('/getPestTreatment/<int:pest_id>', methods=['GET'])
def get_pest_treatment(pest_id):
    try:
        # Query pest treatment by ID
        pest_treatment = Pest_Treatment.query.get_or_404(pest_id)

        # Prepare the pest treatment data
        pest_treatment_data = {
            "PestId": pest_treatment.PestId,
            "Pest_name": pest_treatment.Pest_name,
            "Treat_material": pest_treatment.Treat_material,
            "Treatment": pest_treatment.Treatment,
            "Created_at": pest_treatment.Created_at.strftime('%Y-%m-%d'),
        }

        # If the pest treatment has an image, convert it to base64 string
        if pest_treatment.Image:
            image_data = base64.b64encode(pest_treatment.Image).decode('utf-8')
            pest_treatment_data["Image"] = image_data  # Include base64 image data in the response

        return jsonify({
            "status": 200,
            "message": "Pest treatment fetched successfully",
            "data": pest_treatment_data
        }), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "message": "Failed to fetch pest treatment",
            "error": str(e)
        }), 500