from flask import Blueprint, request, jsonify
from models import User, db
from datetime import datetime
from io import BytesIO
import base64

user_bp = Blueprint('user', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all users
@user_bp.route('/getUsers', methods=['GET'])
def get_users():
    try:
        users = User.query.all()

        result = []
        for u in users:
            user_data = {
                "UserId": u.UserId,
                "Username": u.Username,
                "Email": u.Email,
                "Created_at": u.Created_at.strftime('%Y-%m-%d') if u.Created_at else None,
            }
            # Jika ada gambar, tambahkan gambar dalam format base64
            if u.Pc_image:
                image_data = base64.b64encode(u.Pc_image).decode('utf-8')
                user_data["Image"] = image_data

            result.append(user_data)

        return create_response(data=result, message="Users fetched successfully", status=200)
    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch users", status=500)
    
# Get a specific user by ID (with image as BLOB)
@user_bp.route('/getUser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)

        user_data = {
            "UserId": user.UserId,
            "Username": user.Username,
            "Email": user.Email,
            "Created_at": user.Created_at.strftime('%Y-%m-%d') if user.Created_at else None,
        }

        # Jika ada gambar, tambahkan gambar dalam format base64
        if user.Pc_image:
            image_data = base64.b64encode(user.Pc_image).decode('utf-8')
            user_data["Image"] = image_data

        return create_response(data=user_data, message="User fetched successfully", status=200)
    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch user", status=500)

# Create a new user
@user_bp.route('/createUsers', methods=['POST'])
def create_user():
    try:
        # Mendukung pengunggahan file gambar (form-data)
        username = request.form.get('Username')
        email = request.form.get('Email')
        password = request.form.get('Password')
        created_at = request.form.get('Created_at')
        pc_image_file = request.files.get('Pc_image')

        # Validasi input
        if not all([username, email, password]):
            return create_response(
                error="Missing required fields: 'Username', 'Email', 'Password'",
                message="Invalid request",
                status=400,
            )

        # Handle tanggal otomatis jika tidak diberikan
        if not created_at:
            created_at = datetime.utcnow()

        # Proses file gambar jika ada
        pc_image_blob = None
        if pc_image_file:
            if pc_image_file.content_type not in ['image/jpeg', 'image/png']:
                return create_response(
                    error="Invalid image format. Only JPEG and PNG are allowed",
                    message="Invalid file format",
                    status=400,
                )

            try:
                pc_image_blob = BytesIO(pc_image_file.read()).getvalue()
            except Exception as e:
                return create_response(error=str(e), message="Failed to process the image", status=400)

        # Buat instance User baru
        new_user = User(
            Username=username,
            Email=email,
            Password=password,
            Created_at=created_at,
            Pc_image=pc_image_blob
        )

        # Tambahkan ke database
        db.session.add(new_user)
        db.session.commit()
        return create_response(message="User created successfully", status=201)

    except Exception as e:
        db.session.rollback()
        return create_response(error=str(e), message="Failed to create user", status=500)
