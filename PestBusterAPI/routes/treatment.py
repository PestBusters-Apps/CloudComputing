from flask import Blueprint, request, jsonify
from models import Treatment, db
from datetime import datetime
import os
from io import BytesIO
import base64


treatment_bp = Blueprint('treatment', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all treatments
@treatment_bp.route('/getTreatments', methods=['GET'])
def get_treatments():
    try:
        # Query all treatments from the database
        treatments = Treatment.query.all()

        # Prepare the response data
        result = []
        for treat in treatments:
            treatment_data = {
                "TreatId": treat.TreatId,
                "Treat_material": treat.Treat_material,
                "Treatment": treat.Treatment,
                "Created_at": treat.Created_at.strftime('%Y-%m-%d'),
            }

            # If the treatment has an image, convert it to base64 string
            if treat.Image:
                image_data = base64.b64encode(treat.Image).decode('utf-8')
                treatment_data["Image"] = image_data  # Include base64 image data in the response

            result.append(treatment_data)

        return create_response(data=result, message="Treatments fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch treatments", status=500)

# Get a specific treatment by ID (with image as BLOB)
@treatment_bp.route('/getTreatment/<int:treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    try:
        # Query treatment by ID
        treatment = Treatment.query.get_or_404(treatment_id)

        # Prepare the treatment data
        treatment_data = {
            "TreatId": treatment.TreatId,
            "Treat_material": treatment.Treat_material,
            "Treatment": treatment.Treatment,
            "Created_at": treatment.Created_at.strftime('%Y-%m-%d'),
        }

        # If the treatment has an image, convert it to base64 string
        if treatment.Image:
            treatment_data["Image"] = base64.b64encode(treatment.Image).decode('utf-8')

        return create_response(data=treatment_data, message="Treatment fetched successfully", status=200)

    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch treatment", status=500)

# Add a new treatment with image upload as BLOB
@treatment_bp.route('/createTreatments', methods=['POST'])
def create_treatment():
    if 'Treat_material' not in request.form or 'Treatment' not in request.form or 'Created_at' not in request.form:
        return create_response(
            error="Missing required fields: 'Treat_material', 'Treatment', 'Created_at'",
            message="Invalid request",
            status=400,
        )

    try:
        # Validate and parse the required fields
        treat_material = request.form['Treat_material']
        treatment = request.form['Treatment']
        created_at = request.form['Created_at']

        # Parse datetime for 'Created_at' field
        try:
            created_at = datetime.utcnow()  # Parsing custom format
        except ValueError:
            return create_response(
                error="Invalid 'Created_at' format. Use 'YYYY-MM-DD HH:MM:SS'",
                message="Invalid date format",
                status=400,
            )

        # Handle image file as BLOB (binary data)
        image = request.files.get('Image')  # Optional
        image_blob = None

        if image:
            # Handle file type validation
            if image.content_type not in ['image/jpeg', 'image/png']:
                return create_response(
                    error="Invalid image format. Only JPEG and PNG are allowed",
                    message="Invalid file format",
                    status=400,
                )
            
            # Read the image file as binary data
            try:
                image_blob = BytesIO(image.read()).getvalue()
            except Exception as e:
                return create_response(error=str(e), message="Failed to read image file", status=500)

        # Create new treatment instance with image as BLOB
        new_treatment = Treatment(
            Treat_material=treat_material,
            Treatment=treatment,
            Image=image_blob,  # Save binary data in the database
            Created_at=created_at
        )

        # Add to database
        db.session.add(new_treatment)
        db.session.commit()
        return create_response(message="Treatment created successfully", status=201)

    except Exception as e:
        db.session.rollback()
        return create_response(error=str(e), message="Failed to create treatment", status=500)