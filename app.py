from flask import Flask, request, render_template, Response, redirect
import requests
import configparser
app = Flask(__name__)

# App Routes Defined over here

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about ')
def about():
    return render_template('about.html')


@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Function to get the weather regarding the location
@app.route('/results', methods=['POST'])
def results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp_c = data["main"]["temp"] - 273
    temp = "{0:.2f}".format(temp_c)
    feels_like_c = data["main"]["feels_like"] - 273
    feels_like = "{0:.2f}".format(feels_like_c)
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('weather.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather, flag="wflag")
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_url = base_url + "appid=" + api_key + "&q=" + zip_code
    r = requests.get(api_url)
    return r.json()

# App run
if __name__ == '__main__':
    app.run(host='0.0.0.0')
