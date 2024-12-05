from flask import Blueprint

# Import all blueprints
from .user import user_bp
from .pestdetect import pestdetect_bp
from .pest import pest_bp
from .feedback import feedback_bp
from .treatment import treatment_bp
from .pestTreatment import pest_treatment_bp
from .detectPest import detectPest_bp

# Combine all blueprints into a single function for easy registration
def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(pestdetect_bp, url_prefix='/pestdetects')
    app.register_blueprint(pest_bp, url_prefix='/pests')
    app.register_blueprint(feedback_bp, url_prefix='/feedbacks')
    app.register_blueprint(treatment_bp, url_prefix='/treatments')
    app.register_blueprint(pest_treatment_bp, url_prefix='/pest_treatments')
    app.register_blueprint(detectPest_bp, url_prefix='/detect_pests')
