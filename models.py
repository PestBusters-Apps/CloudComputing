from db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'pb_user'
    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(60), nullable=False)
    Pc_image = db.Column(db.LargeBinary, nullable=True)
    Created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke Feedback dan PestDetect
    feedbacks = db.relationship('Feedback', backref='user_feedback', lazy=True)
    pestdetects = db.relationship('PestDetect', backref='user_detect', lazy=True)

class Feedback(db.Model):
    __tablename__ = 'pb_feedback'
    FeedbackId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('pb_user.UserId'), nullable=False)
    Feedback = db.Column(db.String(255), nullable=False)
    Submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class PestDetect(db.Model):
    __tablename__ = 'pb_pestdetect'
    DetectId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('pb_user.UserId'), nullable=False)
    PestId = db.Column(db.Integer, db.ForeignKey('pb_pest.PestId'), nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)
    Detect_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke tabel User dan Pest
    pest = db.relationship('Pest', backref='pest_detections', lazy=True)

class Pest(db.Model):
    __tablename__ = 'pb_pest'
    PestId = db.Column(db.Integer, primary_key=True)
    Pest_name = db.Column(db.String(60), nullable=False)
    TreatmentId = db.Column(db.Integer, db.ForeignKey('pb_treatment.TreatId'), nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)
    Created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke tabel Treatment
    treatment = db.relationship('Treatment', back_populates='pests')

class Treatment(db.Model):
    __tablename__ = 'pb_treatment'
    TreatId = db.Column(db.Integer, primary_key=True)
    Treat_material = db.Column(db.String(255), nullable=False)
    Treatment = db.Column(db.Text, nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)
    Created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi balik ke tabel Pest
    pests = db.relationship('Pest', back_populates='treatment')


class Pest_Treatment(db.Model):
    __tablename__ = 'pest_treatment_view'
    PestId = db.Column(db.Integer, primary_key=True)
    Pest_name = db.Column(db.String(60), nullable=False)
    Treat_material = db.Column(db.String(255), nullable=False)
    Treatment = db.Column(db.TEXT, nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)
    Created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pest_Detect(db.Model):
    __tablename__ = 'pest_detect_view'
    DetectId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(60), nullable=False)
    Pest_name = db.Column(db.String(60), nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)
    Detect_at = db.Column(db.DateTime, default=datetime.utcnow)