#!/usr/bin/env python
# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from apps.park.models import CarPostion


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for id in range(1, 201):
            postion = CarPostion.objects.filter(id=id).exists()
            if not postion:
                CarPostion.objects.create(id=id)
