from flask import Blueprint, request, Response
from models import db, WeatherRequest
from utils.geocode import geocode_location, parse_gps_coordinates, geocode_zip
from utils.weather_service import getWeatherFromCoordinates
from utils.validate_dates import validate_dates
from utils.location_parser import detect_location_type
from utils.responses import success_response, error_response
from utils.weather_service import getWeatherRange
import json

weather_bp = Blueprint("weather_bp", __name__)


# -------------------------
# Get current weather (NO database write)
# -------------------------
@weather_bp.route("/weather/current", methods=["GET"])
def get_current_weather():

    location = request.args.get("location")

    if not location:
        return error_response("location is required", 400)

    try:

        # detect location type
        location_type = detect_location_type(location)

        if location_type == "gps":
            lat, lon = parse_gps_coordinates(location)

        elif location_type == "ca_postal":
            lat, lon = geocode_zip(location, "CA")

        elif location_type == "us_zip":
            lat, lon = geocode_zip(location, "US")

        else:
            lat, lon = geocode_location(location)

        weather = getWeatherFromCoordinates(lat, lon)
        #print(weather)

        result = {
            "location": location,
            "latitude": lat,
            "longitude": lon,
            "temperature": weather["temperature"],
            "wind_speed": weather["wind_speed"],
            "wind_direction": weather["wind_direction"],
            "weather_code": weather["weather_code"],
            "is_day": weather["is_day"]
        }

        return success_response(result)

    except Exception as e:
        return error_response(str(e), 500)

# -------------------------
# Create Endpoint: Create a new weather record
# -------------------------
@weather_bp.route("/weather", methods=["POST"])
def create_weather():

    data = request.json

    location = data.get("location")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not location or not start_date or not end_date:
        return error_response("location, start_date and end_date required", 400)

    try:

        start_date_obj, end_date_obj = validate_dates(start_date, end_date)

        location_type = detect_location_type(location)

        if location_type == "gps":
            lat, lon = parse_gps_coordinates(location)

        elif location_type == "ca_postal":
            lat, lon = geocode_zip(location, "CA")

        elif location_type == "us_zip":
            lat, lon = geocode_zip(location, "US")

        else:
            lat, lon = geocode_location(location)


        weather = getWeatherRange(lat, lon, start_date, end_date)

        weather_record = WeatherRequest(
            location=location,
            latitude=lat,
            longitude=lon,
            start_date=start_date_obj,
            end_date=end_date_obj,
            temperatures=json.dumps(weather["temperatures"])
        )

        db.session.add(weather_record)
        db.session.commit()

        return success_response({
            "id": weather_record.id,
            "location": location,
            "dates": weather["dates"],
            "temperatures": weather["temperatures"]
        })

    except Exception as e:

        return error_response(str(e), 500)
    

# -------------------------
# Read Endpoint: Read weather records
# -------------------------
@weather_bp.route("/weather", methods=["GET"])
def get_weather():

    location = request.args.get("location")

    if location:

        records = WeatherRequest.query.filter_by(location=location).all()
        if not records:
            return error_response("No records found for this location", 404)

    else:

        records = WeatherRequest.query.all()

    result = [r.to_dict() for r in records]

    return success_response(result)



# -------------------------
# DELETE Endpoint: Delete by ID
# -------------------------
@weather_bp.route("/weather/<int:record_id>", methods=["DELETE"])
def delete_weather(record_id):

    record = WeatherRequest.query.get(record_id)

    if not record:
        return error_response("Record not found", 404)

    db.session.delete(record)
    db.session.commit()

    return success_response({
        "message": f"Record {record_id} deleted"
    })

# -------------------------
# DELETE Endpoint: Delete by location
# -------------------------
@weather_bp.route("/weather/location/<location>", methods=["DELETE"])
def delete_weather_by_location(location):

    records = WeatherRequest.query.filter_by(location=location).all()

    if not records:
        return error_response("No records found for this location", 404)

    deleted_count = len(records)

    for r in records:
        db.session.delete(r)

    db.session.commit()

    return success_response({
        "message": f"{deleted_count} record(s) deleted for location '{location}'"
    })


# -------------------------
# DELETE Endpoint: Delete all records (with safety confirmation)
# -------------------------
@weather_bp.route("/weather/all", methods=["DELETE"])
def delete_all_weather():

    confirm = request.args.get("confirm")

    if confirm != "true":
        return error_response(
            "Safety confirmation required. Use ?confirm=true to delete all records.",
            400
        )

    deleted_count = WeatherRequest.query.count()

    if deleted_count == 0:
        return error_response("Database already empty", 404)

    WeatherRequest.query.delete()
    db.session.commit()

    return success_response({
        "message": f"{deleted_count} record(s) deleted"
    })


# -------------------------
# Update Endpoint: Update a specific weather record
# -------------------------
@weather_bp.route("/weather/<int:record_id>", methods=["PUT"])
def update_weather(record_id):

    record = WeatherRequest.query.get(record_id)

    if not record:
        return error_response("Record not found", 404)

    data = request.json or {}

    try:

        # ----- resolve final values -----

        location = data.get("location", record.location)
        start_date = data.get("start_date", str(record.start_date))
        end_date = data.get("end_date", str(record.end_date))

        # convert date objects if needed
        if isinstance(start_date, str) or isinstance(end_date, str):
            start_date_obj, end_date_obj = validate_dates(start_date, end_date)
        else:
            start_date_obj = start_date
            end_date_obj = end_date

        # ----- resolve location -----

        location_type = detect_location_type(location)

        if location_type == "gps":
            lat, lon = parse_gps_coordinates(location)

        elif location_type == "ca_postal":
            lat, lon = geocode_zip(location, "CA")

        elif location_type == "us_zip":
            lat, lon = geocode_zip(location, "US")

        else:
            lat, lon = geocode_location(location)

        # ----- refresh weather -----

        weather = getWeatherRange(lat, lon, start_date_obj, end_date_obj)

        # ----- update record -----

        record.location = location
        record.latitude = lat
        record.longitude = lon
        record.start_date = start_date_obj
        record.end_date = end_date_obj
        record.temperatures = json.dumps(weather["temperatures"])

        db.session.commit()

        return success_response(record.to_dict())

    except Exception as e:
        return error_response(str(e), 500)
    


# -------------------------
# Export Endpoint: Export all weather records to CSV
# -------------------------
@weather_bp.route("/weather/export/csv", methods=["GET"])
def export_weather_csv():

    records = WeatherRequest.query.all()

    def generate():

        header = [
            "id",
            "location",
            "latitude",
            "longitude",
            "start_date",
            "end_date",
            "temperature",
            "wind_speed",
            "wind_direction",
            "weather_code",
            "is_day",
            "created_at"
        ]

        yield ",".join(header) + "\n"

        for r in records:
            row = [
                str(r.id),
                r.location,
                str(r.latitude),
                str(r.longitude),
                str(r.start_date),
                str(r.end_date),
                str(r.temperature),
                str(r.wind_speed),
                str(r.wind_direction),
                str(r.weather_code),
                str(r.is_day),
                str(r.created_at)
            ]

            yield ",".join(row) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=weather_reports.csv"}
    )


# -------------------------
# Export Endpoint: Export all weather records to Json
# -------------------------
@weather_bp.route("/weather/export/json", methods=["GET"])
def export_weather_json():

    records = WeatherRequest.query.all()

    data = []

    for r in records:
        data.append(r.to_dict())

    return success_response(data)

