# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import unquote
from rest_framework.reverse import reverse

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (Q, Sum)
from django.conf import settings


class Restaurant(models.Model):
    """Model for restaurant."""

    name = models.CharField(
        verbose_name="Name",
        blank=False,
        max_length=100,
    )
    num_seats = models.PositiveIntegerField(
        verbose_name="Number of seats",
        default=10,
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        """Unicode representation."""
        return "Restaurant {name} ({num} seats)".format(
            name=self.name,
            num=self.num_seats,
        )

    def num_seats_available(self, timestamp):
        """Get the number of available seats for a given timestamp."""
        reservations = self.reservations(timestamp)
        if reservations.count() == 0:
            return self.num_seats
        num_reserved = reservations.aggregate(
            Sum('num_guests'),
        ).values()[0]
        return self.num_seats - num_reserved

    def reservations(self, timestamp):
        """Get the reservations for a given timestamp."""
        return self.reservation_set.filter(
            Q(from_time__lte=timestamp),
            Q(to_time__gte=timestamp),
        )

    def reservations_url(self):
        return reverse('reservations', kwargs={
            'restaurant_id': self.id
        })

    def availability_url(self):
        url = reverse('availability', kwargs={
            'restaurant_id': self.pk,
            'datetime': '{datetime}'
        })
        return unquote(url)

    def html_report_url(self):
        return reverse('booking.html', kwargs={
            'restaurant_id': self.pk,
        })

    def json_report_url(self):
        return reverse('booking.json', kwargs={
            'restaurant_id': self.pk,
        })



class Reservation(models.Model):
    """Reservation model."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Name of the reserving guest",
        blank=False,
        max_length=100,
    )
    from_time = models.DateTimeField(
        verbose_name="Start time of reservation",
    )
    to_time = models.DateTimeField(
        verbose_name="End time of reservation",
    )
    num_guests = models.PositiveIntegerField(
        verbose_name="Number of guests",
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        """Unicode representation."""
        return (
            "Reservation for {name} at {restaurant}: {num} guests from {start}"
            " to {end}"
        ).format(
            name=self.name,
            restaurant=self.restaurant.name,
            num=self.num_guests,
            start=self.from_time.strftime(settings.DATETIME_FORMAT),
            end=self.to_time.strftime(settings.DATETIME_FORMAT),
        )

