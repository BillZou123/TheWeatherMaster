from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json

db = SQLAlchemy()


class WeatherRequest(db.Model):

    __tablename__ = "weather_requests"

    id = db.Column(db.Integer, primary_key=True)

    # user input
    location = db.Column(db.String(100), nullable=False)

    # resolved coordinates
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # date range
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # forecast data (stored as JSON string)
    temperatures = db.Column(db.Text, nullable=False)

    # metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            "id": self.id,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "temperatures": json.loads(self.temperatures),
            "created_at": self.created_at.isoformat()
        }