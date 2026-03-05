from flask import Flask, send_from_directory
from backend.routes.weather_routes import weather_bp
from backend.models import db
from backend.config import FRONTEND_DIR

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#create db tables
with app.app_context():
    db.create_all()

#register blueprint
app.register_blueprint(weather_bp)

# -------------------------
# Serve frontend
# -------------------------
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)