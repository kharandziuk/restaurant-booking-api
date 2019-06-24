from rest_framework import serializers
from . import models


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = (
            'name',
            'restaurant',
            'from_time',
            'to_time',
            'num_guests',
        )
