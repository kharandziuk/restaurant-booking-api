import datetime
from urllib.parse import unquote

from rest_framework.reverse import reverse
from rest_framework import serializers


from django.utils.timezone import make_aware
from django.conf import settings

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
    def validate(self, data):
        if (
                data['restaurant'].num_seats_available(data['from_time']) -
                data['num_guests']
            ) < 0:
            raise serializers.ValidationError("not enough space")
        return super().validate(data)

class RestaurantSerializer(serializers.ModelSerializer):
    reservations_url = serializers.SerializerMethodField()
    availability_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Restaurant
        fields = (
            'name',
            'num_seats',
            'reservations_url',
            'availability_url'
        )

    def get_reservations_url(self, obj):
        return '{0}'.format(reverse('reservations', kwargs={
            'restaurant_id': obj.id
        }))

    def get_availability_url(self, obj):
        url = '{0}'.format(reverse('availability', kwargs={
            'restaurant_id': obj.id,
            'datetime': '{datetime}'
        }))
        return unquote(url)

class AvailabilitySerializer(serializers.ModelSerializer):
    seats_available = serializers.SerializerMethodField()

    class Meta:
        model = models.Restaurant
        fields = (
            'id',
            'seats_available'
        )

    def get_seats_available(self, obj) :
        _datetime = self.context['datetime']
        try:
            _datetime = make_aware(
                datetime.datetime.strptime(_datetime, settings.DATETIME_FORMAT)
            )
        except ValueError:
            raise serializers.ValidationError('datetime in a wrong format')
        return obj.num_seats_available(_datetime)


class RestaurantBookingSerializer(serializers.ModelSerializer):
    reservation_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Restaurant
        fields = (
            'name',
            'num_seats',
            'reservation_set'
        )
