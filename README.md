# TheWeatherMaster


## Author
Yuangan Zou  

---

# Project Overview

This project is a **full-stack weather application** that allows users to search for weather conditions by entering a city name, ZIP code, or GPS location.

The application retrieves real-time weather data and displays:

- Current temperature
- Wind speed
- Wind direction
- Weather conditions
- Multi-day weather forecast
- Location map visualization

The system integrates **external APIs**, **geolocation services**, and **interactive UI components** to provide a smooth weather lookup experience.

---


# Live Demo

Deployed application:

https://theweathermaster2.onrender.com/

Note: This application uses the **OpenWeather API**, which is a free public weather API. Since the app is deployed on Render, all API requests originate from a shared Render server IP. Free API tiers may enforce request limits per IP, so if the limit is reached by other users on the same server, the weather request may temporarily fail. If this happens, please try again later.

# Features

### Weather Search
Users can enter a:

- City name
- ZIP code
- GPS location

The app will retrieve the **current weather conditions** for that location.

### Current Weather Information
The app displays:

- Temperature (°C)
- Wind speed
- Wind direction
- Weather condition code
- Daytime status

### Weather Forecast
A **multi-day forecast** is displayed showing:

- Weather icons
- Daily high and low temperatures

### Location Map
A map is automatically generated to show the **searched location**.

### Use My Location
Users can retrieve weather information using **browser geolocation**.

---

# Technology Stack

Frontend
- HTML
- CSS
- JavaScript

Backend
- Python
- Flask

External APIs
- Weather API (weather data)
- Geocoding API (location coordinates)
- Google Maps Embed API (map visualization)

Deployment
- Render Cloud Hosting

---

# Installation

## 1. Clone the repository

git clone https://github.com/YOUR_USERNAME/weather-app.git

cd weather-app



## 2. Install dependencies

pip3 install -r requirements.txt

## 3. Start Flask server

cd backend

python3 app.py

---

# API Endpoints
The backend exposes several REST API endpoints that handle weather data retrieval and geolocation services.
All endpoints return responses in JSON format.

⸻

## 1. Get Current Weather

Retrieve the current weather information for a specific location.

**Endpoint**  
GET /weather/current

**Query Parameters**

| Parameter | Type | Description |
|---|---|---|
| location | string | Location name, GPS coordinates, Canadian postal code, or US ZIP code |

**Example Request**  
GET /weather/current?location=North%20York

**Example Response**
```json
{
  "location": "North York",
  "latitude": 43.7615,
  "longitude": -79.4111,
  "temperature": 5.1,
  "wind_speed": 25.2,
  "wind_direction": 76,
  "weather_code": 3,
  "is_day": true
}
```

---

## 2. Create Weather Record

Create a weather record for a specific location and date range. This endpoint fetches weather data and stores it in the database.

**Endpoint**  
POST /weather

**Body Parameters**

| Parameter | Type | Description |
|---|---|---|
| location | string | Location name, GPS coordinates, Canadian postal code, or US ZIP code |
| start_date | string | Start date in `YYYY-MM-DD` format |
| end_date | string | End date in `YYYY-MM-DD` format |

**Example Request**
```http
POST /weather
Content-Type: application/json

{
  "location": "Toronto",
  "start_date": "2024-01-01",
  "end_date": "2024-01-05"
}
```

**Example Response**
```json
{
  "id": 1,
  "location": "Toronto",
  "dates": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
  "temperatures": [-2.3, -1.8, -3.0, -0.5, 1.2]
}
```

---

## 3. Get Weather Records

Retrieve weather records stored in the database. You can optionally filter by location.

**Endpoint**  
GET /weather

**Query Parameters**

| Parameter | Type | Description |
|---|---|---|
| location | string | Optional. Filter records by location |

**Example Request**  
GET /weather?location=Toronto

**Example Response**
```json
[
  {
    "id": 1,
    "location": "Toronto",
    "latitude": 43.6532,
    "longitude": -79.3832,
    "start_date": "2024-01-01",
    "end_date": "2024-01-05",
    "temperatures": "[ -2.3, -1.8, -3.0, -0.5, 1.2 ]"
  }
]
```

---

## 4. Update Weather Record

Update an existing weather record by ID. If `location` or date range is changed, the weather data will be refreshed.

**Endpoint**  
PUT /weather/{record_id}

**Body Parameters**

| Parameter | Type | Description |
|---|---|---|
| location | string | Optional. New location |
| start_date | string | Optional. Start date in `YYYY-MM-DD` |
| end_date | string | Optional. End date in `YYYY-MM-DD` |

**Example Request**
```http
PUT /weather/1
Content-Type: application/json

{
  "location": "Vancouver",
  "start_date": "2024-01-01",
  "end_date": "2024-01-03"
}
```

**Example Response**
```json
{
  "id": 1,
  "location": "Vancouver",
  "latitude": 49.2827,
  "longitude": -123.1207,
  "start_date": "2024-01-01",
  "end_date": "2024-01-03",
  "temperatures": "[5.2, 6.1, 7.0]"
}
```

---

## 5. Delete Weather Record by ID

Delete a weather record using its ID.

**Endpoint**  
DELETE /weather/{record_id}

**Example Request**  
DELETE /weather/1

**Example Response**
```json
{
  "message": "Record 1 deleted"
}
```

---

## 6. Delete Weather Records by Location

Delete all weather records for a specific location.

**Endpoint**  
DELETE /weather/location/{location}

**Example Request**  
DELETE /weather/location/Toronto

**Example Response**
```json
{
  "message": "3 record(s) deleted for location 'Toronto'"
}
```

---

## 7. Delete All Weather Records

Delete all weather records from the database. Requires confirmation for safety.

**Endpoint**  
DELETE /weather/all

**Query Parameters**

| Parameter | Type | Description |
|---|---|---|
| confirm | string | Must be `true` to confirm deletion |

**Example Request**  
DELETE /weather/all?confirm=true

**Example Response**
```json
{
  "message": "10 record(s) deleted"
}
```

---

## 8. Export Weather Records (CSV)

Export all weather records as a CSV file.

**Endpoint**  
GET /weather/export/csv

**Example Request**  
GET /weather/export/csv

**Example Response**
```csv
id,location,latitude,longitude,start_date,end_date,temperature,wind_speed,wind_direction,weather_code,is_day,created_at
1,Toronto,43.6532,-79.3832,2024-01-01,2024-01-05,5.2,12.3,120,3,true,2024-01-10
```

---

## 9. Export Weather Records (JSON)

Export all weather records as JSON.

**Endpoint**  
GET /weather/export/json

**Example Request**  
GET /weather/export/json

**Example Response**
```json
[
  {
    "id": 1,
    "location": "Toronto",
    "latitude": 43.6532,
    "longitude": -79.3832,
    "start_date": "2024-01-01",
    "end_date": "2024-01-05",
    "temperatures": "[5.2, 6.1, 7.0]"
  }
]
```








# About PM Accelerator

The **Product Manager Accelerator (PM Accelerator)** is a professional development program designed to help aspiring product managers build real-world product and technical skills.

The program focuses on helping participants:

- Understand product development processes
- Build working applications
- Learn how software products are designed and delivered
- Demonstrate technical and problem-solving abilities

Participants complete hands-on technical projects that showcase their ability to build and deploy functional software systems.

More information about the PM Accelerator program can be found on their LinkedIn page.

---








