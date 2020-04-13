from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import time


def homepage(request):
    if request.method == "POST":

        print(request.POST)

        form = request.POST.get('search-box')

        if form is not None:

            if len(form) > 0:
                location = ",".join(form.split())

                if weather_data(location) is not None:

                    return render(request, 'weather/homepage.html', weather_data(location))

                else:
                    return render(request, 'weather/unknown.html')

        else:
            return render(request, 'weather/unknown.html')

    return render(request, 'weather/homepage.html', weather_data(None))


def weather_data(location):
    file_path = r"apikey.txt"

    api_key = open(file_path, 'r').read().strip()

    website = f"http://api.openweathermap.org/data/2.5/forecast?q={'london,uk' if location is None else location}&appid={api_key}"

    weather_report = requests.get(website).json()

    check_location = weather_report.get('message')

    if check_location != "city not found":

        content = {'data': {'country': f"{weather_report['city']['name']}, {weather_report['city']['country']}"},
                   'full_data': {},
                   'hourly_data': {}

                   }

        date_checker = ''

        for index, hourly_report in enumerate(weather_report['list']):

            weather_info = hourly_report['dt_txt'].split()[0]

            epoch_time = hourly_report.pop('dt')

            kev_temp = hourly_report['main'].pop('temp')

            celsius = {'temp': int(kev_temp - 273.15)}

            hourly_report['main'].update(celsius)

            timeNow = time.strftime('%A %H:%M %p', time.localtime(epoch_time))

            hourly_report['dt'] = timeNow

            if weather_info != date_checker:
                date_checker = weather_info
                content['data'][str(index)] = hourly_report

            day = timeNow.split()[0]
            retrieve_time = hourly_report['dt_txt'].split()[1]

            if day not in content['full_data']:

                content['full_data'][day] = [hourly_report]

            else:
                hourly_report['time'] = retrieve_time
                content['full_data'][day].append(hourly_report)

            if retrieve_time not in content['hourly_data']:

                content['hourly_data'][retrieve_time] = [hourly_report]

            else:
                content['hourly_data'][retrieve_time].append(hourly_report)

        data_info_by_hour = content.pop('hourly_data')

        sorting_hour = {key: value for key, value in sorted(data_info_by_hour.items())}

        content['hourly_data'] = sorting_hour


        return content

    else:

        return None


def weather_about(request):
    return render(request, 'weather/about.html')
