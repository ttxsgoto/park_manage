#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from rest_framework import routers
from .views import MemberViewSet, CarPostionViewSet, MemberAmountViewSet, TempAmountViewSet

park_router = routers.DefaultRouter()
park_router.register(r'members', MemberViewSet, 'members')
park_router.register(r'car_postions', CarPostionViewSet, 'car_postions')
park_router.register(r'member_amount', MemberAmountViewSet, 'member_amount')
park_router.register(r'temp_amount', TempAmountViewSet, 'temp_amount')

urlpatterns = park_router.urls
