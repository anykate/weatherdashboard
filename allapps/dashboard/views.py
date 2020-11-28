from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City
from django.conf import settings
import requests
from time import timezone


# Create your views here.
def get_weather_data(city_name):
    url = 'https://api.openweathermap.org/data/2.5/weather/'

    params = {
        'q': city_name,
        'appid': settings.OWM_API_KEY,
        'units': 'metric',
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return

    json_response = response.json()

    weather_data = {
        'temp': json_response['main']['temp'],
        'temp_min': json_response['main']['temp_min'],
        'temp_max': json_response['main']['temp_max'],
        'city_name': json_response['name'],
        'country': json_response['sys']['country'],
        'lat': json_response['coord']['lat'],
        'lon': json_response['coord']['lon'],
        'weather': json_response['weather'][0]['main'],
        'weather_desc': json_response['weather'][0]['description'],
        'pressure': json_response['main']['pressure'],
        'humidity': json_response['main']['humidity'],
        'wind_speed': json_response['wind']['speed'],
    }

    return weather_data


def index(request):
    weather_data = request.session.get('weather_data', False)
    if weather_data:
        del request.session['weather_data']

    form = CityForm(request.POST or None)

    if not weather_data and request.method == 'GET':
        try:
            name = City.objects.latest('updated_at').name
            weather_data = get_weather_data(name)
        except Exception as e:
            weather_data = get_weather_data('Pune')

    if form.is_valid():
        form.save(commit=False)
        name = form.cleaned_data['name']
        weather_data = get_weather_data(name)
        request.session['weather_data'] = weather_data
        if weather_data:
            try:
                city = City.objects.get(name=name.capitalize())
                city.name = name
                city.save()
            except Exception as e:
                City.objects.create(name=name.capitalize())
        return redirect('dashboard:index')
    return render(request, 'dashboard/index.html', {'form': form, 'weather_data': weather_data})
