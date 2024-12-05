from flask import Blueprint, request, jsonify
from models import Feedback, db
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

def create_response(data=None, message=None, error=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }
    return jsonify(response), status

# Get all feedbacks
@feedback_bp.route('/getFeedbacks', methods=['GET'])
def get_feedbacks():
    try:
        feedbacks = Feedback.query.all()
        result = []

        for fb in feedbacks:
            feedback_data = {
                "FeedbackId": fb.FeedbackId,
                "User": {
                    "UserId": fb.user_feedback.UserId,
                    "Username": fb.user_feedback.Username
                },
                "Feedback": fb.Feedback,
                "Submitted_at": fb.Submitted_at.strftime('%Y-%m-%d') if fb.Submitted_at else None
            }
            result.append(feedback_data)

        return create_response(data=result, message="Feedbacks fetched successfully", status=200)
    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch feedbacks", status=500)
    
# Get a specific feedback by ID
@feedback_bp.route('/getFeedback/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        feedback_data = {
            "FeedbackId": feedback.FeedbackId,
            "User": {
                "UserId": feedback.user_feedback.UserId,
                "Username": feedback.user_feedback.Username
            },
            "Feedback": feedback.Feedback,
            "Submitted_at": feedback.Submitted_at.strftime('%Y-%m-%d') if feedback.Submitted_at else None
        }

        return create_response(data=feedback_data, message="Feedback fetched successfully", status=200)
    except Exception as e:
        return create_response(error=str(e), message="Failed to fetch feedback", status=500)

# Add a new feedback
@feedback_bp.route('/createFeedbacks', methods=['POST'])
def create_feedback():
    try:
        
        user_id = request.form.get('UserId')
        feedback = request.form.get('Feedback')

        # Validasi input
        if not user_id or not feedback:
            return create_response(
                error="Missing required fields: 'UserId' and 'Feedback'",
                message="Invalid request",
                status=400,
            )

        # Buat instance Feedback baru
        new_feedback = Feedback(
            UserId=user_id,
            Feedback=feedback,
        )

        # Simpan ke database
        db.session.add(new_feedback)
        db.session.commit()

        return create_response(message="Feedback created successfully", status=201)
    except Exception as e:
        db.session.rollback()
        return create_response(error=str(e), message="Failed to create feedback", status=500)
