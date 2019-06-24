# -*- coding: utf-8 -*-
from rest_framework import mixins
from rest_framework import generics

from . import serializers, models

class ReservationList(mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        restaurant_id =  self.kwargs.get('restaurant_id')
        return super().get_queryset().filter(restaurant=restaurant_id)


class RestaurantList(mixins.ListModelMixin,
        generics.GenericAPIView):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
