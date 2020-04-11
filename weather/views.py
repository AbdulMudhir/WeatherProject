from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import time


def homepage(request):
    website = "http://api.openweathermap.org/data/2.5/forecast?q=london,uk&appid="

    weather_report = requests.get(website).json()

    # print(test)
    #
    # for i in test:
    #     print(i,test[i])

    content = {'data':
                   {'country': f"{weather_report['city']['name']}, {weather_report['city']['country']}"}

               }

    date_checker = ''



    for index, hourly_report in enumerate(weather_report['list']):

        weather_data = hourly_report['dt_txt'].split()[0]

        if weather_data != date_checker:
            date_checker = weather_data

            epoch_time = hourly_report.pop('dt')

            kev_temp = hourly_report['main'].pop('temp')

            celsius ={'temp': int(kev_temp - 273.15)}

            hourly_report['main'].update(celsius)

            timeNow = time.strftime('%A %H:%M %p', time.localtime(epoch_time))

            hourly_report['dt'] = timeNow

            content['data'][str(index)] = hourly_report
    return render(request, 'weather/homepage.html', content)


def weather_about(request):
    return render(request, 'weather/about.html')
