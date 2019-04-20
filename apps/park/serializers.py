#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.park.models import Member, CarPostion, MemberAmount, TempAmount
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]


class MemberListSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def to_representation(self, instance):
        data = super(MemberListSerializer, self).to_representation(instance)
        data['creator_name'] = instance.creator.username
        postion = instance.get_postion
        postion_id = postion.id if postion else ''
        data['postion_id'] = postion_id
        data['member_type_ch'] = '包年' if instance.type == 'year' else '包季'
        data['type_ch'] = dict(Member.CAR_TYPE).get(instance.type, '')
        return data


class MemberSerializer(ModelSerializer):
    postion_id = serializers.IntegerField(max_value=200, min_value=1, required=False, help_text='车位ID')

    class Meta:
        model = Member
        exclude = ('expire_time', 'creator')

    def validate(self, attrs):
        plate_number = attrs['plate_number']
        identity_card = attrs['identity_card']
        postion_id = attrs['postion_id']
        if Member.objects.filter(plate_number=plate_number).exists():
            raise serializers.ValidationError('车牌号已存在')
        if len(identity_card) != 18:
            raise serializers.ValidationError('身份证号码必须为18位')
        if Member.objects.filter(identity_card=attrs['identity_card']).exists():
            raise serializers.ValidationError('身份证号码已存在')
        if postion_id:
            postion = CarPostion.objects.filter(id=postion_id).first()
            if not postion or not postion.is_valid:
                raise serializers.ValidationError('当前车位不能使用')
            attrs['postion_id'] = postion
        return attrs

    def create(self, validated_data):
        postion = validated_data.pop('postion_id', None)
        plate_number = validated_data.get('plate_number', '')
        request = self.context['request']
        instance = super(MemberSerializer, self).create(validated_data)
        if postion:
            member_type = instance.member_type
            expire_time = instance.created_time + relativedelta(
                years=1) if member_type == 'year' else instance.created_time + relativedelta(months=3)
            instance.expire_time = expire_time
            instance.creator = request.user
            instance.save()
            MemberAmount.objects.create(
                member=instance,
                money=600.00 if member_type == 'year' else 300.00
            )
            postion.member = instance
            postion.is_member = True
            postion.is_valid = False
            postion.plate_number = plate_number
            postion.save()
        return instance


class CarPostionSerializer(ModelSerializer):
    class Meta:
        model = CarPostion
        fields = '__all__'

    def to_representation(self, instance):
        data = super(CarPostionSerializer, self).to_representation(instance)
        data['member'] = MemberListSerializer(instance.member).data if instance.member else {}
        data['is_member_ch'] = '是' if instance.is_member else '否'
        data['is_valid_ch'] = '是' if instance.is_valid else '否'
        return data


class MemberAmountSerializer(ModelSerializer):
    class Meta:
        model = MemberAmount
        fields = '__all__'

    def to_representation(self, instance):
        data = super(MemberAmountSerializer, self).to_representation(instance)
        data['member'] = MemberListSerializer(instance.member).data if instance.member else {}
        return data


class TempAmountListSerializer(ModelSerializer):
    class Meta:
        model = TempAmount
        fields = '__all__'

    def to_representation(self, instance):
        data = super(TempAmountListSerializer, self).to_representation(instance)
        data['creator_name'] = instance.creator.username
        data['is_member_ch'] = '是' if instance.is_member else '否'
        return data


class TempAmountSerializer(ModelSerializer):
    class Meta:
        model = TempAmount
        exclude = ('creator', 'is_member', 'postion')

        read_only_fields = ('leave_time',)

    def validate(self, attrs):
        plate_number = attrs['plate_number']
        if TempAmount.objects.filter(plate_number=plate_number,
                                     leave_time__isnull=True,
                                     enter_time__lte=datetime.now()
                                     ).exists():
            raise serializers.ValidationError('该车辆已在停车场')
        member = Member.objects.filter(plate_number=plate_number,
                                       expire_time__gte=datetime.now()
                                       ).first()
        is_member = True if member else False
        attrs['is_member'] = is_member
        if is_member:
            postion = member.get_postion
        else:
            postion = CarPostion.objects.filter(is_valid=True).first()
            if not postion:
                raise serializers.ValidationError('没有可用停车位')
        attrs['postion'] = postion
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        plate_number = validated_data.get('plate_number', '')
        is_member = validated_data.get('is_member', '')
        postion = validated_data.get('postion', None)
        instance = super(TempAmountSerializer, self).create(validated_data)
        instance.creator = request.user
        instance.save()
        if not is_member:
            postion.is_valid = False
            postion.plate_number = plate_number
            postion.save()
        return instance
