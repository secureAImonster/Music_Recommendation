//Problem: Make a weather app that will recive current wether with country and postal code
//Solve: Get API from http://openweathermap.org/ and make interactive search for weather using console
const API_KEY = "dc96fb1fc220527e0ccd89436c36d259";

var http = require('http');

function getWeatherPrecipitation(weather_code) {
	var precipitaion = 0;
	switch(parseInt(weather_code)){
		case 1:
		//clear
			precipitation = 0.75;
			break;

		case 2:
		//few clouds
			precipitation = 0.6;
			break;

		case 3:
		//scattered clouds    
			precipitation = 0.5;
			break;

		case 4:
		//broken clouds
		    precipitation = 0.4;
			break;

		case 5:
		//shower rain
		    precipitation = 0.3;
			break;

		case 6:
		//rain
		    precipitation = 0.25;
			break;

		default:
		//rain
		    precipitation = 0.25;
			
	}
	return precipitation;
}

function getWeatherInfo(weatherAPI) {
	var temp = Math.round((weatherAPI.main.temp-273.15)*100)/100;	
	var icon_string = weatherAPI.weather[0].icon; 
	var weather = getWeatherPrecipitation(icon_string.substring(1,2)); 

	return {
		city: weatherAPI.name,
		weather: weather,
		temp: String(temp) 
	}
}

//Print out error messages
function printError(error) {
	console.error(error.message);
}

//Connect to the API URL api.openweathermap.org/data/2.5/weather?q={city name},{country code}
function get(city,callback){
    var request = http.get('http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid='+ API_KEY, function(response) {
		var body = '';

		//Read the data
		response.on('data', function(chunk) {
			body += chunk;
		});

		response.on('end', function() {
			if (response.statusCode === 200) {
				try {
					//Parse the data
					var weatherAPI = JSON.parse(body);
					var result = getWeatherInfo(weatherAPI);
					callback(result);
				} catch(error) {
					//Parse error
					printError(error);
				}
			} else {
				//Status Code error
				printError({message: 'There was an error getting the weather from ' + city + '. (' + http.STATUS_CODES[response.statusCode] + ')'});
			}
		})
	});

	//Connection error
	request.on('error', function (err) {
		printError(err);
	});

};

module.exports = {
	get: get
};
