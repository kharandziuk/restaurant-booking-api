from rest_framework.reverse import reverse
from rest_framework import serializers
from . import models


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = (
            'id',
            'name',
            'restaurant',
            'from_time',
            'to_time',
            'num_guests',
        )

class RestaurantSerializer(serializers.ModelSerializer):
    reservations_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Restaurant
        fields = (
            'name',
            'num_seats',
            'reservations_url'
        )

    def get_reservations_url(self, obj):
        return '{0}'.format(reverse('reservations', kwargs={
            'restaurant_id': obj.id
        }))
