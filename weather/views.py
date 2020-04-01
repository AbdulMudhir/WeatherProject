from django.shortcuts import render
from django.http import HttpResponse



def weather_homepage(request):

    return render(request, 'weather/homepage.html')


def weather_about(request):
    return render(request, 'weather/about.html')
