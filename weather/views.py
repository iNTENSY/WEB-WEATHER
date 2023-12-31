from typing import Any

import requests
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from weather.forms import FindCityForm
from weather.models import Cities
from weather.tasks import counter
from weather.mixins import UrlMixin


class WeatherPageView(UrlMixin, generic.FormView):
    form_class = FindCityForm
    template_name: str = 'base.html'
    DEFAULT_CITY: str = 'Moscow'

    def get(self, *args, **kwargs) -> render:
        """
        Данный метод обрабатывает GET запрос как с помощью вставки
        города в строку запроса, так и обработку с помощью формы.
        """
        if self.kwargs.get('city'):
            request = requests.get(self.OPENWEATHERMAP_URL.format(self.kwargs['city'])).json()
            if request['cod'] == '404':
                return render(
                    self.request,
                    self.template_name,
                    {'code_status': 'denied', 'city': 'Ваш город не был распознан!'}
                )
            self.start_task(self.kwargs.get('city'))
        else:
            user_ip: str = self.get_client_ip(request=self.request)
            geolocation_data: dict = self.get_geolocation_data(user_ip)
            if geolocation_data['status'] == 'success':
                request: dict = self.get_weatherdata_for_city(geolocation_data['city'])
                self.start_task(geolocation_data['city'])
            else:
                request: dict = self.get_weatherdata_for_city(self.DEFAULT_CITY)
        return render(self.request, self.template_name, self.get_context_data(data=request))

    def post(self, *args, **kwargs):
        """
        Данный метод используется, когда пользователь запросил данные
        с помощью специальной формы. После этого, программа
        использует redirect на главную страницу.
        """
        city = self.request.POST.get('name')
        if city:
            return redirect(reverse('weather:page_for_find_city_by_name', kwargs={'city': city}))
        return redirect(reverse('weather:first_page'))

    def get_geolocation_data(self, ip: str):
        """
        Данный метод получает и возвращает ответ от API сервиса
        в формате JSON, определяя в нем город с которого произошел запрос.
        """
        data = requests.get(self.FIND_CITY_BY_IP_URL.format(ip)).json()
        return data

    def get_weatherdata_for_city(self, city: str):
        """
        Данный метод получает и возвращает ответ от API сервиса
        в формате JSON, определяя в нем данные с погодой в городе.
        """
        data = requests.get(self.OPENWEATHERMAP_URL.format(city)).json()
        return data

    def get_context_data(self, data: dict = None) -> dict:
        """
        Переопределение родительского метода, для добавления в него
        удобного формата вывода погоды, статуса погоды и температуру запрашиваемого города.
        """
        context: dict[str, Any] = super(WeatherPageView, self).get_context_data()
        if data is not None and data['cod'] != '404':
            context['code_status'] = 'access'
            context['weatherdata'] = data
            context['city'] = context['weatherdata']['name']
            context['weather_status'] = context['weatherdata']['weather'][0]['description']
            context['weather_temp'] = round(context['weatherdata']['main']['temp'])
        return context

    @staticmethod
    def start_task(city: str) -> None:
        """Данный метод вызывает параллельную задачу."""
        counter.delay(city)

    @staticmethod
    def get_client_ip(request) -> str:
        """Определение IP пользователя, от которого пришел request."""
        x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip: str = x_forwarded_for.split(',')[0]
        else:
            ip: str = request.META.get('REMOTE_ADDR')
        return ip


class RedirectToView(generic.RedirectView):
    """Данный класс перенаправляет пользователя на домашнюю страницу."""
    def get_redirect_url(self, *args, **kwargs) -> str:
        return reverse_lazy('weather:first_page')


@method_decorator(cache_page(60*5), name='dispatch')
class RatingView(generic.ListView):
    template_name: str = 'weather/rating.html'
    context_object_name: str = 'cities'

    def get_queryset(self):
        q: QuerySet[Cities] = Cities.objects.all().order_by('-total_searches')[:10]
        return q

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context: dict[str, Any] = super().get_context_data()
        context['form'] = FindCityForm()
        return context
