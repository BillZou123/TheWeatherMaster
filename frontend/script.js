


function getWeatherIcon(code, isDay){

    if(code === 0) return isDay ? "☀️" : "🌙"
    if(code <= 3) return "⛅"
    if(code <= 48) return "☁️"
    if(code <= 67) return "🌧️"
    if(code <= 77) return "❄️"
    if(code <= 82) return "🌦️"
    if(code <= 99) return "⛈️"

    return "🌍"
}

function showError(message){

    const errorBox = document.getElementById("errorPopup")

    errorBox.innerText = message
    errorBox.style.display = "block"

    setTimeout(()=>{
        errorBox.style.display = "none"
    }, 3000)

}

async function getWeather(){

    const location = document.getElementById("location").value

    try{

        const url = `/weather/current?location=${location}`
        const response = await fetch(url)
        const data = await response.json()

        // 如果后端返回 error
        if(data.status === "error"){
            showError(data.message)
            return
        }

        const weather = data.data

        const icon = getWeatherIcon(weather.weather_code, weather.is_day)

        const html = `
            <div class="weather-card">

                <div class="weather-icon">${icon}</div>

                <div class="temp">${weather.temperature} °C</div>

                <div class="weather-details">
                    <div>Wind Speed: ${weather.wind_speed} km/h</div>
                    <div>Wind Direction: ${weather.wind_direction}°</div>
                    <div>Daytime: ${weather.is_day ? "Yes" : "No"}</div>
                    <div>Weather Code: ${weather.weather_code}</div>
                </div>

            </div>
        `

        document.getElementById("weatherResult").innerHTML = html

        const lat = weather.latitude
        const lon = weather.longitude

        const mapHTML = `
            <iframe
                class="map-frame"
                loading="lazy"
                allowfullscreen
                src="https://www.google.com/maps?q=${lat},${lon}&output=embed">
            </iframe>
        `

        document.getElementById("mapContainer").innerHTML = mapHTML

    }
    catch(error){

        showError("Unable to fetch weather data. Please try again.")

    }

}


async function getCurrentLocationWeather(){

    if (!navigator.geolocation){
        alert("Geolocation not supported")
        return
    }

    navigator.geolocation.getCurrentPosition(async function(position){

        const lat = position.coords.latitude
        const lon = position.coords.longitude

        

        const url =
        "https://api.open-meteo.com/v1/forecast"
        + `?latitude=${lat}`
        + `&longitude=${lon}`
        + "&daily=temperature_2m_max,temperature_2m_min,weathercode"
        + "&timezone=auto"

        const response = await fetch(url)
        const data = await response.json()

        const daily = data.daily

        let html = `<div class="forecast-container">`

        for(let i=0;i<5;i++){

            const icon = getWeatherIcon(daily.weathercode[i], true)

            const day =
            new Date(daily.time[i])
            .toLocaleDateString(undefined,{weekday:'short'})

            html += `
            <div class="forecast-card">

                <div class="forecast-day">
                    ${day}
                </div>

                <div class="forecast-icon">
                    ${icon}
                </div>

                <div class="forecast-temp">
                    ${daily.temperature_2m_max[i]}° /
                    ${daily.temperature_2m_min[i]}°
                </div>

            </div>
            `
        }

        html += `</div>`

        document.getElementById("currentLocationWeather").innerHTML = html

    })
}