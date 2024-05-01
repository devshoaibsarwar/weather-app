
# Weather Forecast

## Description:

Weather Forecast is a Django project designed to get `current` and `3-hourly/5 days` weather data based on user' location. User has to input longitude & latitude and select the type of forecast he/she wants 

## Setup:

To set up the project, follow these steps:

### Using Virtual Environment (venv):

Create a virtual environment:
```
python -m venv venv
```
Activate the virtual environment:
```
source venv/bin/activate
```
Install dependencies from requirements.txt:
```
pip install -r requirements.txt
```

## Running the Server:

Before running server, execute the following command to collect the static files in the project:
```
python manage.py collectstatic
```

To run the server, execute the following command:
```
python manage.py runserver
```

## Usage:
Use this weather app to access current weather and forecasts powered by OpenWeatherAPI. Simply run the server, 
navigate to http://127.0.0.1:8000 in your browser, input longitude, latitude, and forecast type, and get instant weather updates.

## Dependencies:
```
Django==2.2
djangorestframework==3.12.2
requests==2.31.0
django-environ==0.11.2
pytest==8.1.1
pytest-django==4.8.0
```

## Running Tests:

To run the test cases, ensure `pytest` and `pytest-django` are installed. Then, execute the following command in the project root directory:

```
pytest
```
Note: Make sure to have the project dependencies installed and the server running before making requests to the APIs.
