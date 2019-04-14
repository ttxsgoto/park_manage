#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

import django_filters
from apps.park.models import CarPostion, Member, TempAmount


class CarPostionFilter(django_filters.FilterSet):
    class Meta:
        model = CarPostion
        fields = ['is_member', 'is_valid', 'id']


class TempAmountFilter(django_filters.FilterSet):
    created_time_start = django_filters.DateTimeFilter(name='created_time', lookup_expr='gte')
    created_time_end = django_filters.DateTimeFilter(name='created_time', lookup_expr='lte')

    class Meta:
        model = TempAmount
        fields = ['plate_number', 'created_time_start', 'created_time_end']


class MemberFilter(django_filters.FilterSet):
    plate_number = django_filters.CharFilter(name='plate_number', lookup_expr='icontains')
    username = django_filters.CharFilter(name='username', lookup_expr='icontains')

    class Meta:
        model = Member
        fields = ['plate_number', 'username']
