# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
import pytest
import factory
import datetime

from . import factories


pytestmark = pytest.mark.django_db

def reverseq(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url


def test_can_receive_list_of_the_reservations_for_a_restaurant(django_app):
    restaurant = factories.RestaurantFactory()
    factories.ReservationFactory(restaurant=restaurant)
    other_reservation = factories.ReservationFactory()
    response = django_app.get(
        reverseq('reservations', query_kwargs={'restaurant': restaurant.id})
    )
    assert response.status_code == 200
    assert len(response.json) == 1
    assert not other_reservation.id in [r['id'] for r in response.json]

def test_can_receive_list_of_the_reservations_for_a_restaurant_with_shortcut(django_app):
    restaurant = factories.RestaurantFactory()
    factories.ReservationFactory(restaurant=restaurant)
    other_reservation = factories.ReservationFactory()
    response = django_app.get(
        reverse('restaurant-reservations', kwargs={'restaurant_id': restaurant.id})
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
        'reservations_url': restaurant.reservations_url(),
        'availability_url': restaurant.availability_url(),
        'html_report_url': restaurant.html_report_url(),
        'json_report_url': restaurant.json_report_url(),
    }]

def test_can_create_reservation_for_a_restaurant(django_app):
    restaurant = factories.RestaurantFactory()
    response = django_app.get(reverse('restaurants'))
    assert response.status_code == 200
    _reservation = factories.ReservationFactory.build()
    print(response.json[0]['reservations_url'])
    response = django_app.post_json(
        response.json[0]['reservations_url'],
        dict(
            name=_reservation.name,
            num_guests=_reservation.num_guests,
            from_time=_reservation.from_time.isoformat(),
            to_time=_reservation.to_time.isoformat()
        )
    )
    assert response.status_code == 201
    assert restaurant.reservation_set.count() == 1

def test_cant_create_reservation_for_mt_available_seats(django_app):
    restaurant = factories.RestaurantFactory()
    factories.ReservationFactory(restaurant=restaurant)
    response = django_app.get(reverse('restaurants'))
    assert response.status_code == 200
    _reservation = factories.ReservationFactory.build()
    response = django_app.post_json(
        response.json[0]['reservations_url'],
        dict(
            name=_reservation.name,
            num_guests=restaurant.num_seats + 1,
            from_time=_reservation.from_time.isoformat(),
            to_time=_reservation.to_time.isoformat()
        ),
        expect_errors=True,
    )
    assert response.status_code == 400
    assert response.json == {'non_field_errors': ['not enough space']}

def test_cant_check_availability_with_datetime_in_wrong_format(django_app):
    restaurant = factories.RestaurantFactory()
    response = django_app.get(reverse('restaurants'))
    availability_url_pattern = response.json[0]['availability_url']
    formated_now = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
    response = django_app.get(
        availability_url_pattern.format(datetime=30034),
        expect_errors=True,
    )
    assert response.status_code == 400
    assert response.json == ['datetime in a wrong format']

def test_can_check_availability_for_a_restaurant(django_app):
    restaurant = factories.RestaurantFactory()
    response = django_app.get(reverse('restaurants'))
    availability_url_pattern = response.json[0]['availability_url']
    formated_now = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
    response = django_app.get(
        availability_url_pattern.format(datetime=formated_now)
    )
    assert response.status_code == 200
    assert response.json == {'id': 1, 'seats_available': 10}

def test_can_check_bookings_for_restaurant_json(django_app):
    restaurant = factories.RestaurantFactory()
    factories.ReservationFactory(restaurant=restaurant)
    factories.ReservationFactory(restaurant=restaurant)
    factories.ReservationFactory(restaurant=restaurant)
    response = django_app.get(reverse('booking.json', kwargs=dict(restaurant_id=restaurant.id)))
    assert response.status_code == 200
    assert response.json['name'] == 'Restaurant 009'
    assert response.json['num_seats'] == 10
    assert len(response.json['reservation_set']) == 3

def test_can_check_bookings_for_restaurant_html(django_app):
    restaurant = factories.RestaurantFactory()
    reservation = factories.ReservationFactory(restaurant=restaurant)
    response = django_app.get(reverse('booking.html', kwargs=dict(restaurant_id=restaurant.id)))
    assert response.status_code == 200
    assert restaurant.name in response.text
    assert reservation.name in response.text
