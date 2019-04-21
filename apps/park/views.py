#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import logging
import math

from datetime import datetime

from django.db.models import Sum
from rest_framework import decorators
from rest_framework.response import Response
from apps.park.filters import CarPostionFilter, MemberFilter, TempAmountFilter, MemberAmountFilter
from apps.park.models import Member, CarPostion, MemberAmount, TempAmount
from apps.park.serializers import MemberSerializer, CarPostionSerializer, MemberListSerializer, MemberAmountSerializer, \
    TempAmountSerializer, TempAmountListSerializer, UserSerializer
from core.mixins import ModelViewSet, ListModelMixin, APIGenericViewSet, CreateModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)


class UserViewSet(ListModelMixin, APIGenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'msg': '获取成功',
            'data': serializer.data
        })


class MemberViewSet(ModelViewSet):
    """会员"""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_class = MemberFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MemberListSerializer
        return super(MemberViewSet, self).get_serializer_class()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({
                'code': -1,
                'msg': '参数错误'
            })
        plate_number = request.data.get('plate_number', '')
        identity_card = request.data.get('identity_card', '')
        username = request.data.get('username', '')
        phone = request.data.get('phone', '')
        member_type = request.data.get('member_type', '')
        type = request.data.get('type', '')
        color = request.data.get('color', '')

        if plate_number and Member.objects.filter(plate_number=plate_number).exclude(id=instance.id).exists():
            return Response({
                'code': -1,
                'msg': '车牌号已存在'
            })
        if identity_card and Member.objects.filter(identity_card=identity_card).exclude(id=instance.id).exists():
            return Response({
                'code': -1,
                'msg': '身份证号码已存在'
            })
        instance.username = username if username else instance.username
        instance.phone = phone if phone else instance.phone
        instance.identity_card = identity_card if identity_card else instance.identity_card
        instance.plate_number = plate_number if plate_number else instance.plate_number
        instance.member_type = member_type if member_type else instance.member_type
        instance.type = type if type else instance.type
        instance.color = color if color else instance.color
        instance.creator = request.user
        instance.save()
        CarPostion.objects.filter(member=instance).update(
            is_member=True, is_valid=False, plate_number=plate_number
        )
        return Response({
            'code': 0,
            'msg': '修改成功',
        })


class CarPostionViewSet(ListModelMixin, APIGenericViewSet):
    """车位"""
    queryset = CarPostion.objects.all()
    serializer_class = CarPostionSerializer
    filter_class = CarPostionFilter


class MemberAmountViewSet(ListModelMixin, APIGenericViewSet):
    """会员金额"""
    queryset = MemberAmount.objects.all()
    serializer_class = MemberAmountSerializer
    filter_class = MemberAmountFilter

    def list(self, request, *args, **kwargs):
        amount_data = super(MemberAmountViewSet, self).list(request, *args, **kwargs)
        created_time_start = request.GET.get('created_time_start', None)
        created_time_end = request.GET.get('created_time_end', None)
        plate_number = request.GET.get('plate_number', None)
        creator = request.GET.get('creator', None)
        if created_time_start and created_time_end and creator and plate_number:
            member_queryset = MemberAmount.objects.filter(created_time__gte=created_time_start,
                                                          created_time__lte=created_time_end,
                                                          member__creator_id=creator,
                                                          member__carpostion__plate_number__contains=plate_number,
                                                          )
            temp_queryset = TempAmount.objects.filter(created_time__gte=created_time_start,
                                                      created_time__lte=created_time_end,
                                                      creator_id=creator,
                                                      plate_number__contains=plate_number
                                                      )
        elif created_time_start and created_time_end and creator:
            member_queryset = MemberAmount.objects.filter(created_time__gte=created_time_start,
                                                          created_time__lte=created_time_end,
                                                          member__creator_id=creator
                                                          )
            temp_queryset = TempAmount.objects.filter(created_time__gte=created_time_start,
                                                      created_time__lte=created_time_end,
                                                      creator_id=creator
                                                      )
        elif created_time_start and created_time_end and plate_number:
            member_queryset = MemberAmount.objects.filter(created_time__gte=created_time_start,
                                                          created_time__lte=created_time_end,
                                                          member__carpostion__plate_number__contains=plate_number
                                                          )
            temp_queryset = TempAmount.objects.filter(created_time__gte=created_time_start,
                                                      created_time__lte=created_time_end,
                                                      plate_number__contains=plate_number
                                                      )
        elif created_time_start and created_time_end:
            member_queryset = MemberAmount.objects.filter(created_time__gte=created_time_start,
                                                          created_time__lte=created_time_end,
                                                          )
            temp_queryset = TempAmount.objects.filter(created_time__gte=created_time_start,
                                                      created_time__lte=created_time_end,
                                                      )
        else:
            member_queryset = MemberAmount.objects.all()
            temp_queryset = TempAmount.objects.all()

        member_sum = member_queryset.aggregate((Sum('money')))
        temp_sum = temp_queryset.aggregate(Sum('money'))
        _member_sum = member_sum.get('money__sum') if member_sum.get(
            'money__sum') else 0
        _temp_sum = temp_sum.get('money__sum') if temp_sum.get(
            'money__sum') else 0
        all_sum = _member_sum + _temp_sum
        return Response({
            'code': 0,
            'msg': '获取成功',
            'data': amount_data.data['data'],
            'all_sum': all_sum
        })


class TempAmountViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, APIGenericViewSet):
    """停车收费"""
    queryset = TempAmount.objects.all()
    serializer_class = TempAmountSerializer
    filter_class = TempAmountFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TempAmountListSerializer
        return super(TempAmountViewSet, self).get_serializer_class()

    @decorators.action(methods=['post'], detail=False, url_path='leave')
    def leave(self, request, *args, **kwargs):
        """离开停车收费"""
        plate_number = request.data.get('plate_number', '')
        tempamount = TempAmount.objects.filter(plate_number=plate_number,
                                               enter_time__lte=datetime.now(),
                                               leave_time__isnull=True
                                               ).first()
        if tempamount:
            now_time = datetime.now()
            diff_time = now_time - tempamount.enter_time
            days = diff_time.days
            if days != 0:
                day_time = days * 24
                days_amout = days * 24 * 2
            else:
                day_time = 0
                days_amout = 0
            diff_hour = diff_time.seconds / 60 / 60
            hour_num = math.modf(diff_hour)
            int_num = hour_num[1]
            decimal_num = 0.5 if hour_num[0] < 0.5 else 1.0
            hour = int_num + decimal_num
            member = Member.objects.filter(plate_number=plate_number,
                                           expire_time__gte=now_time
                                           )
            is_member = True if member.exists() else False
            tempamount.leave_time = now_time
            tempamount.time_duration = hour + day_time
            tempamount.save()
            if is_member:
                return Response({
                    'code': 0,
                    'is_member': True,
                    'amount': 0
                })
            else:
                postion = tempamount.postion
                if postion:
                    postion.is_valid = True
                    postion.plate_number = ''
                    postion.member = None
                    postion.save()
                if (diff_time.seconds / 60) < 30:
                    return Response({
                        'code': 0,
                        'is_member': False,
                        'msg': '停车时间小于30分钟',
                        'amount': 0
                    })
                else:
                    tempamount.money = 2 * hour + days_amout
                    tempamount.save()
                    return Response({
                        'code': 0,
                        'is_member': False,
                        'msg': '停车时间大于30分钟',
                        'amount': 2 * hour + days_amout
                    })
        return Response({
            'code': -1,
            'msg': '车辆不存在停车场'
        })
