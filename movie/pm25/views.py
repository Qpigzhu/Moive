from django.shortcuts import render
from .api_pm import main
# Create your views here.


def home(requets):
    context = {}
    return render(requets,'home.html',context)


def pa(request):
    context = {}
    error_msg = ''
    city_name = request.GET.get('city')

    if not city_name:
        error_msg = '请输入关键词'
        context['error_msg'] = error_msg
        return render(request, 'pm25.html',context)

    aqi_list = main(city_name)
    context = {}
    context['aqi_list'] = aqi_list
    context['aqi'] = aqi_list[0]
    context['city_name'] = aqi_list[1]
    context['affect'] = aqi_list[2]
    context['action'] = aqi_list[3]
    return render(request,'pm25.html',context)

