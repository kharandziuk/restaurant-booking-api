# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
import pytest

from . import factories


pytestmark = pytest.mark.django_db

def test_can_receive_list_of_the_reservations_for_a_restaurant(django_app):
    restaurant = factories.RestaurantFactory()
    factories.ReservationFactory(restaurant=restaurant)
    other_reservation = factories.ReservationFactory()
    response = django_app.get(
        reverse('reservations', kwargs={'restaurant_id': restaurant.id})
    )
    assert response.status_code == 200
    assert len(response.json) == 1
    assert not other_reservation.id in [r['id'] for r in response.json]

def test_can_receive_list_of_the_restaurants(django_app):
    restaurant = factories.RestaurantFactory()
    response = django_app.get(reverse('restaurants'))
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json == [{
        'name': restaurant.name,
        'num_seats': restaurant.num_seats,
        'reservations_url':
            reverse('reservations', kwargs={'restaurant_id': restaurant.pk})
    }]

