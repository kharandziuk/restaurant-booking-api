import datetime
import factory

from . import models
from django.utils.timezone import make_aware

class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Restaurant

    name = factory.Sequence(lambda n: "Restaurant %03d" % n)


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reservation

    name = factory.Sequence(lambda n: "Reservation %03d" % n)
    restaurant = factory.SubFactory(RestaurantFactory)
    from_time = factory.LazyFunction(lambda : make_aware(datetime.datetime.now()))
    num_guests = 2
    to_time = factory.LazyFunction(
        lambda : make_aware(datetime.datetime.now() + datetime.timedelta(hours=1))
    )



