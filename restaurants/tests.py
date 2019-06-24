# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
import pytest

from . import factories


pytestmark = pytest.mark.django_db

def test_can_receive_list_with_a_reservation(django_app):
    print(reverse('reservations'))
    factories.ReservationFactory()
    response = django_app.get(reverse('reservations'))
    assert response.status_code == 200
    assert len(response.json) == 1

