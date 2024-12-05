from flask import Flask
from db import init_app, db
from routes import register_routes

def create_app():
    app = Flask(__name__)

    # Konfigurasi database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@host/database'  # Ganti dengan URI database Anda
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi database
    init_app(app)

    # Registrasi semua route
    register_routes(app)

    # Debug routes
    print(f"{'Endpoint':<30} {'URL':<50}")  # Header with column names
    print("-" * 80)  # Divider line for clarity

    for rule in app.url_map.iter_rules():
        # Printing endpoint and URL in table format with alignment
        print(f"{rule.endpoint:<30} {str(rule):<50}")

    return app

if __name__ == '__main__':
    app = create_app()

    # Buat tabel di database jika belum ada
    with app.app_context():
        db.create_all()

    # Jalankan aplikasi
    app.run(debug=True)
