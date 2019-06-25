# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers, models


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return super().get_queryset().filter(restaurant=restaurant_id)

    def create(self, request, *args, **kwargs):
        request.data['restaurant'] = restaurant_id = kwargs.get('restaurant_id')
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
