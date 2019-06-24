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

