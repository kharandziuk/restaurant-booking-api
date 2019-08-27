# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import serializers, models


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        restaurant_id = self.request.query_params.get('restaurant', None)
        if restaurant_id:
            queryset = queryset.filter(restaurant=restaurant_id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['restaurant'] = request.query_params.get('restaurant')
        return super().create(request, *args, **kwargs)


class RestaurantReservationsForwardView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print('here')
        request.GET = request.GET.copy()
        request.GET['restaurant'] = kwargs.get('restaurant_id')
        return ReservationViewSet.as_view(dict(get='list', post='create'))(request)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        restaurant_id = self.request.query_params.get('restaurant', None)
        if restaurant_id:
            queryset = queryset.filter(restaurant=restaurant_id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['restaurant'] = request.query_params.get('restaurant')
        return super().create(request, *args, **kwargs)


class AvailabilityView(generics.RetrieveAPIView):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.AvailabilitySerializer
    lookup_url_kwarg = 'restaurant_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['datetime'] = self.kwargs.get('datetime')
        return context


class RestaurantBookingJSONView(generics.RetrieveAPIView):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantBookingSerializer
    lookup_url_kwarg = 'restaurant_id'


class RestaurantBookingHTMLView(RestaurantBookingJSONView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'booking.html'
