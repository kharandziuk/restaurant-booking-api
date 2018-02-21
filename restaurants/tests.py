# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

from .models import (
    Restaurant,
    Reservation,
)

class RestaurantReservationTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Testaurant",
            num_seats=20,
        )

    def tearDown(self):
        self.restaurant.delete()

    def test_booking(self):
        time = datetime(2018, 05, 23, 20, 30)
        res_1 = Reservation.objects.create(
            restaurant=self.restaurant,
            name="Reservation 1",
            from_time=datetime(2018, 05, 23, 20, 00),
            to_time=datetime(2018, 05, 23, 22, 00),
            num_guests=10
        )
        self.assertEqual(self.restaurant.reservations(time).count(), 1)
        self.assertEqual(self.restaurant.num_seats_available(time), 10)
        res_2 = Reservation.objects.create(
            restaurant=self.restaurant,
            name="Reservation 2",
            from_time=datetime(2018, 05, 23, 20, 00),
            to_time=datetime(2018, 05, 23, 22, 00),
            num_guests=5
        )
        res_3 = Reservation.objects.create(
            restaurant=self.restaurant,
            name="Reservation 3",
            from_time=datetime(2018, 05, 23, 19, 00),
            to_time=datetime(2018, 05, 23, 20, 00),
            num_guests=10
        )
        self.assertEqual(self.restaurant.reservations(time).count(), 2)
        self.assertEqual(self.restaurant.num_seats_available(time), 5)

