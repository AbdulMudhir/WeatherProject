from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import time


def homepage(request):
    if request.method == "POST":

        form = request.POST['search-box']

        if len(form) > 0:
            location = ",".join(form.split())

            if weather_data(location) is not None:

                return render(request, 'weather/homepage.html', weather_data(location))

            else:
                return render(request, 'weather/unknown.html')

    return render(request, 'weather/homepage.html', weather_data(None))


def weather_data(location):
    file_path = r"C:\Users\Abdul\PycharmProjects\WeatherProject\apikey.txt"

    api_key = open(file_path, 'r').read().strip()

    website = f"http://api.openweathermap.org/data/2.5/forecast?q={'london,uk' if location is None else location}&appid={api_key}"

    weather_report = requests.get(website).json()

    check_location = weather_report.get('message')

    if check_location != "city not found":

        content = {'data':
                       {'country': f"{weather_report['city']['name']}, {weather_report['city']['country']}"}

                   }

        date_checker = ''

        for index, hourly_report in enumerate(weather_report['list']):

            weather_info = hourly_report['dt_txt'].split()[0]

            if weather_info != date_checker:
                date_checker = weather_info

                epoch_time = hourly_report.pop('dt')

                kev_temp = hourly_report['main'].pop('temp')

                celsius = {'temp': int(kev_temp - 273.15)}

                hourly_report['main'].update(celsius)

                timeNow = time.strftime('%A %H:%M %p', time.localtime(epoch_time))

                hourly_report['dt'] = timeNow

                content['data'][str(index)] = hourly_report

        return content

    else:

        return None


def weather_about(request):
    return render(request, 'weather/about.html')
