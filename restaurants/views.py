# -*- coding: utf-8 -*-
from rest_framework import viewsets

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
