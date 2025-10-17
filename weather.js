//So to get current weather for London: 
// JSON: http://api.weatherapi.com/v1/current.json?key=<YOUR_API_KEY>&q=London

//To get 7 day weather for US Zipcode 07112: 
// JSON: http://api.weatherapi.com/v1/forecast.json?key=<YOUR_API_KEY>&q=07112&days=7


key = "005186776a4c4589a6e90608250407";
url ="https://api.weatherapi.com/v1";

const locationInput = document.getElementById('cityInput');
const searchButton = document.getElementById('search');
const retryButton = document.getElementById('retry');
const getCity = document.getElementById('city');
const getRegion = document.getElementById('region');
const getCountry = document.getElementById('country');
const getTemperature = document.getElementById('temperature');
const getDescription = document.getElementById('description');
const loadingOverlay = document.getElementById('loading');
const errorMessage = document.getElementById('error');

//default city
window.onload = () => {
    fetchWeather("New Delhi");
}



searchButton.addEventListener('click',() => {
    const location = locationInput.value;
    if (location){
        fetchWeather(location);
    }
});
locationInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        searchButton.click();
    }
});

async function fetchWeather(location){

    //------------------for Current Weather-------------------------------
    const currentWeatherURL= `${url}/current.json?key=${key}&q=${location}`;

    try {
        const response = await fetch(currentWeatherURL);
        if (response.ok) {
            const data = await response.json();
            displayWeather(data);
        }
    } catch (error) {
        console.log("Error fetching data", error);
    }


    //------------------for hourly data----------------------------------
    const hourNow = new Date().getHours();
    const hourDisplay = 24 - hourNow;
    if(hourDisplay == 0){
        hourDisplay = 24;
    }

    let i=1;
    while(i<(hourDisplay+1)){
        const forecastHourlyURL= `${url}/forecast.json?key=${key}&q=${location}&hour=${hourNow}+${i}`;
        try {
            const response = await fetch(forecastHourlyURL);
            if (response.ok) {
                const data = await response.json();
                displayHourlyForecast(data); 
            }
        } catch (error) {
            console.log("Error fetching data", error);
        }
        i++;
    }

    //-----------------------for 10 days data----------------------------
    const forecastURL= `${url}/forecast.json?key=${key}&q=${location}&days=10`;

    try {
        const response = await fetch(forecastURL);
        if (response.ok) {
            const data = await response.json();
            displayDaywiseForecast(data); 
        }
    } catch (error) {
        console.log("Error fetching data", error);
    }
}

//general data
function displayWeather(data){

    // for Current Weather
    getCity.textContent= data.location.name;
    getRegion.textContent= data.location.region;
    getCountry.textContent= data.location.country;
    getTemperature.textContent = `${data.current.temp_c}°C`;
    getDescription.textContent = data.current.condition.text;

    var imageAdd = document.createElement("img");
    imageAdd.src = `https:${data.current.condition.icon}`;
    imageAdd.alt = data.current.condition.text;
    getTemperature.appendChild(imageAdd);
}

//hourly weather data
function displayHourlyForecast(data){

    const hourlyForecastContainer = document.getElementById('hour');
    hourlyForecastContainer.innerHTML = ''; 
    const todayHourlyForecast = data.forecast.forecastday[0].hour; //today's hourly data

    const currentHour = new Date(data.location.localtime).getHours();

    todayHourlyForecast.forEach(hourData => {
        const hour = new Date(hourData.time).getHours();
    
        if (hour > currentHour) {
            const hourlyCard = document.createElement('div');
            hourlyCard.classList.add('hData-card');
            hourlyCard.innerHTML = `
                <p class="time">${hour}</p>
                <img src="https:${hourData.condition.icon}" alt="${hourData.condition.text}" />
                <p class="temp">${hourData.temp_c}°C</p>
            `;
            hourlyForecastContainer.appendChild(hourlyCard);
        }
    });
}

//daywise weather
function displayDaywiseForecast(data){

    const dayWiseForecastContainer = document.getElementById('day');
    dayWiseForecastContainer.innerHTML = ''; 
    const forecastCollection = data.forecast.forecastday;
   
    forecastCollection.forEach(forecastData => {
        const forecastCard = document.createElement('div');
        forecastCard.classList.add('dayData-card');
        forecastCard.innerHTML = `
            <p class="date">${forecastData.date}</p>
            <img src="https:${forecastData.day.condition.icon}" alt="${forecastData.day.condition.text}" />
            <p class="temp">${forecastData.day.maxtemp_c}°C / ${forecastData.day.mintemp_c}°C </p>
        `;
        dayWiseForecastContainer.appendChild(forecastCard);
    });
}