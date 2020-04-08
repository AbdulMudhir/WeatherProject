from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse


class Homepage(TemplateView):
    template_name = "weather/homepage.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)

#
# def weather_homepage(request):
#     if request.POST:
#         content = request.POST['search-box']
#
#         print(content)
#
#     return render(request, 'weather/homepage.html')
#

def weather_about(request):
    return render(request, 'weather/about.html')
