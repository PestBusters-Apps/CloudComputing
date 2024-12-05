from flask import Blueprint, request, jsonify
from models import Pest, Treatment, db
from datetime import datetime
from io import BytesIO
import base64

pest_bp = Blueprint('pest', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all pests
@pest_bp.route('/getPests', methods=['GET'])
def get_pests():
    try:
        pests = Pest.query.all()

        result = []
        for pest in pests:
            pest_data = {
                "PestId": pest.PestId,
                "Pest_name": pest.Pest_name,
                "TreatmentId": pest.treatment.Treatment if pest.treatment else None,
                "Created_at": pest.Created_at.strftime('%Y-%m-%d') if pest.Created_at else None
            }

            # If the pest has an image, convert it to base64 string
            if pest.Image:
                image_data = base64.b64encode(pest.Image).decode('utf-8')
                pest_data["Image"] = image_data

            result.append(pest_data)

        return create_response(data=result, message="Pests fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch pests", status=500)
    
# Get a specific pest by ID (with image as BLOB)
@pest_bp.route('/getPest/<int:pest_id>', methods=['GET'])
def get_pest(pest_id):
    try:
        pest = Pest.query.get_or_404(pest_id)

        pest_data = {
            "PestId": pest.PestId,
            "Pest_name": pest.Pest_name,
            "TreatmentId": pest.TreatmentId,
            "Created_at": pest.Created_at.strftime('%Y-%m-%d') if pest.Created_at else None
        }

        # If the pest has an image, convert it to base64 string
        if pest.Image:
            image_data = base64.b64encode(pest.Image).decode('utf-8')
            pest_data["Image"] = image_data

        return create_response(data=pest_data, message="Pest fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch pest", status=500)
        

# Add a new pest with image upload as BLOB
@pest_bp.route('/createPests', methods=['POST'])
def create_pest():
    if 'Pest_name' not in request.form or 'TreatmentId' not in request.form or 'Created_at' not in request.form:
        return create_response(
            error="Missing required fields: 'Pest_name', 'TreatmentId', 'Created_at'",
            message="Invalid request",
            status=400,
        )

    try:
        # Extract form data
        pest_name = request.form.get('Pest_name')
        treatment_id = request.form.get('TreatmentId')
        created_at = request.form.get('Created_at')

        # Parse datetime
        try:
            created_at = datetime.utcnow()
        except ValueError:
            return create_response(
                error="Invalid 'Created_at' format. Use 'YYYY-MM-DD HH:MM:SS'",
                message="Invalid date format",
                status=400,
            )

        # Validate TreatmentId
        treatment = Treatment.query.get(treatment_id)
        if not treatment:
            return create_response(
                error="Invalid 'TreatmentId'. Treatment not found",
                message="Invalid request",
                status=400,
            )

        # Handle image file as BLOB (binary data)
        image = request.files.get('Image')
        image_blob = None
        if image:
            # Handle file type validation
            if image.content_type not in ['image/jpeg', 'image/png']:
                return create_response(
                    error="Invalid image format. Only JPEG and PNG are allowed",
                    message="Invalid file format",
                    status=400,
                )
            
            try:
                # Read the image as binary data
                image_blob = BytesIO(image.read()).getvalue()
            except Exception as e:
                return create_response(
                    error="Failed to read image file",
                    message="Invalid file data",
                    status=400,
                )

        # Create new pest instance
        new_pest = Pest(
            Pest_name=pest_name,
            TreatmentId=treatment_id,  # Save the foreign key
            Image=image_blob,  # Save binary data in the database
            Created_at=created_at
        )

        # Add to database
        db.session.add(new_pest)
        db.session.commit()
        return create_response(message="Pest created successfully", status=201)

    except Exception as e:
        # Rollback if there's an error
        db.session.rollback()
        return create_response(error=str(e), message="Failed to create pest", status=500)
