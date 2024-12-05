from flask import Blueprint, request, jsonify
from models import PestDetect, User, Pest, db
from io import BytesIO
import base64
from datetime import datetime

pestdetect_bp = Blueprint('pestdetect', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Add a new pest detection
@pestdetect_bp.route('/createPestdetects', methods=['POST'])
def create_pestdetect():
    try:
        # Mendukung pengunggahan file gambar (form-data)
        user_id = request.form.get('UserId')
        pest_id = request.form.get('PestId')
        image_file = request.files.get('Image')

        # Validasi input
        if not all([user_id, pest_id]):
            return create_response(
                error="Missing required fields: 'UserId', 'PestId'",
                message="Invalid request",
                status=400,
            )

        # Validasi apakah user dan pest ada
        user = User.query.get(user_id)
        pest = Pest.query.get(pest_id)
        if not user or not pest:
            return create_response(
                error="Invalid 'UserId' or 'PestId'. User or Pest not found",
                message="Invalid request",
                status=404,
            )

        # Proses file gambar jika ada
        image_blob = None
        if image_file:
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return create_response(
                    error="Invalid image format. Only JPEG and PNG are allowed",
                    message="Invalid file format",
                    status=400,
                )

            try:
                image_blob = BytesIO(image_file.read()).getvalue()
            except Exception as e:
                return create_response(error=str(e), message="Failed to process the image", status=500)

        # Buat instance PestDetect baru
        new_pestdetect = PestDetect(
            UserId=user_id,
            PestId=pest_id,
            Image=image_blob,
            Detect_at=datetime.utcnow(),  # Waktu otomatis diisi dengan waktu saat ini
        )

        # Tambahkan ke database
        db.session.add(new_pestdetect)
        db.session.commit()
        return create_response(message="Pest detection created successfully", status=201)

    except Exception as e:
        db.session.rollback()
        return create_response(error=str(e), message="Failed to create pest detection", status=500)
