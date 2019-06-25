from django.core.management.base import BaseCommand
from restaurants import factories

class Command(BaseCommand):
    help = 'Adds initial data'

    def handle(self, *args, **options):
        for _ in range(4):
            restaurant = factories.RestaurantFactory()
            for _ in range(3):
                factories.ReservationFactory(restaurant=restaurant)
