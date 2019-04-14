#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import logging
import math

from datetime import datetime

from rest_framework import decorators
from rest_framework.response import Response
from apps.park.filters import CarPostionFilter, MemberFilter, TempAmountFilter
from apps.park.models import Member, CarPostion, MemberAmount, TempAmount
from apps.park.serializers import MemberSerializer, CarPostionSerializer, MemberListSerializer, MemberAmountSerializer, \
    TempAmountSerializer, TempAmountListSerializer
from core.mixins import ModelViewSet, ListModelMixin, APIGenericViewSet, CreateModelMixin, UpdateModelMixin, \
    RetrieveModelMixin

logger = logging.getLogger(__name__)


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
            tempamount.time_duration = hour
            tempamount.save()
            if is_member:
                return Response({
                    'code': 0,
                    'is_member': True,
                    'amount': 0
                })
            else:
                # diff_time = now_time - tempamount.enter_time
                # 停车位释放掉， 可被其他车辆使用
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
                    return Response({
                        'code': 0,
                        'is_member': False,
                        'msg': '停车时间大于30分钟',
                        'amount': 2 * hour
                    })
        return Response({
            'code': -1,
            'msg': '车辆不存在停车场'
        })
