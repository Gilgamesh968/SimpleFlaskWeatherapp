from flask import Flask, render_template, redirect, request, url_for, flash
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


app =  Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        api_key = '30d4741c779ba94c470ca1f63045390a'
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={api_key}")    
        try:
            if weather_data.json()['cod'] == '404':
                flash('City not found', category='error')
            else:
                temp = weather_data.json()['main']['temp']
                tempC = round((temp-32) * (5/9))
                weather = weather_data.json()['weather'][0]['main']
                data = weather_data.json()['cod']
                return render_template('weather.html', temp=temp, weather=weather, data=data, city=city_name, tempC=tempC)
        except KeyError:
            flash('Key error, city name cannot be empty', category='error')
    
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)