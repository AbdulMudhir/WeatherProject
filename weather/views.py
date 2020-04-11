from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import time


def homepage(request):
    website = "http://api.openweathermap.org/data/2.5/weather?q=london,uk&appid=39834b9c3a416570d2846cb396d2d22e"

    weather_report = requests.get(website).json()

    timeNow = time.strftime('%A %H:%M %p', time.localtime(weather_report['dt']))

    content = {'name': weather_report['name'],
               'country': weather_report['sys']['country'],
               'temperature': int(weather_report['main']['temp'] - 273.15),
               'weather': weather_report['weather'][0]['main'],
               'description': weather_report['weather'][0]['description'],
               'pressure': weather_report['main']['pressure'],
               'humidity': weather_report['main']['humidity'],
               'wind': weather_report['wind']['speed'],
               'sunrise': weather_report['sys']['sunrise'],
               'sunset': weather_report['sys']['sunset'],
               'timezone': weather_report['timezone'],
               'timeNow': timeNow,
               'icon': f"{weather_report['weather'][0]['icon']}"
               }

    if request.method == "POST":

        form = request.POST['search-box']

        if len(form) > 0:

            location = ",".join(form.split())

            website = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=39834b9c3a416570d2846cb396d2d22e"

            weather_report = requests.get(website).json()

            check_location = weather_report.get('message')

            if check_location is None:

                timeNow = time.strftime('%A %H:%M %p', time.localtime(weather_report['dt']))

                content = {'name': weather_report['name'],
                           'country': weather_report['sys']['country'],
                           'temperature': int(weather_report['main']['temp'] - 273.15),
                           'weather': weather_report['weather'][0]['main'],
                           'description': weather_report['weather'][0]['description'],
                           'pressure': weather_report['main']['pressure'],
                           'humidity': weather_report['main']['humidity'],
                           'wind': weather_report['wind']['speed'],
                           'sunrise': weather_report['sys']['sunrise'],
                           'sunset': weather_report['sys']['sunset'],
                           'timezone': weather_report['timezone'],
                           'timeNow': timeNow,
                           'icon': f"{weather_report['weather'][0]['icon']}"
                           }

                return render(request, 'weather/homepage.html', content)

            else:

                timeNow = time.strftime('%A %H:%M %p', time.localtime(time.time()))

                return render(request, 'weather/unknown.html', {'timeNow':timeNow})

    return render(request, 'weather/homepage.html', content)


def weather_about(request):
    return render(request, 'weather/about.html')
