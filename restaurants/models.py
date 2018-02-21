# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (Q, Sum)


class Restaurant (models.Model):
    name = models.CharField(verbose_name="Name", blank=False, max_length=100)
    num_seats = models.PositiveIntegerField(
        verbose_name="Number of seats",
        default=10,
        validators=[MinValueValidator(1)])

    def __unicode__(self):
        return "Restaurant {name} ({num} seats)".format(name=self.name, num=self.num_seats)

    def num_seats_available(self, time):
        num_reserved = self.reservations(time).aggregate(Sum('num_guests')).values()[0]
        return self.num_seats - num_reserved

    def reservations(self, time):
        return self.reservation_set.filter(Q(from_time__lte=time), Q(to_time__gte=time))


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name of the reserving guest", blank=False, max_length=100)
    from_time = models.DateTimeField(verbose_name="Start time of reservation")
    to_time = models.DateTimeField(verbose_name="End time of reservation")
    num_guests = models.PositiveIntegerField(verbose_name="Number of guests", validators=[MinValueValidator(1)])

    def __unicode__(self):
        return "Reservation for {name} at {restaurant}: {num} guests from {start} to {end}".format(
            name=self.name,
            restaurant=self.restaurant.name,
            num=self.num_guests,
            start=self.from_time,
            end=self.to_time,
        )