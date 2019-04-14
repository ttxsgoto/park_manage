#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Member(models.Model):
    CAR_TYPE = (
        (1, '轿车'),
        (2, 'SUV'),
        (3, 'MPV'),
        (4, '跑车'),
        (5, '皮卡'),
        (6, '微面')

    )
    MEMBER_TYPE = (
        ('quarter', '包季'),
        ('year', '包年')
    )
    username = models.CharField('用户名', max_length=128)
    phone = models.CharField('手机号码', max_length=12, null=True, blank=True, default='')
    identity_card = models.CharField('身份证', max_length=18)
    plate_number = models.CharField('车牌号', max_length=32)
    member_type = models.CharField('会员类型', max_length=32, choices=MEMBER_TYPE, default='quarter')
    type = models.IntegerField('类型', choices=CAR_TYPE, default=1)
    color = models.CharField('颜色', max_length=32, null=True, blank=True, default='')
    expire_time = models.DateTimeField('到期时间', null=True, blank=True, default=None)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    creator = models.ForeignKey(User, null=True, blank=True, default=None)

    class Meta:
        db_table = 'members'
        verbose_name = 'members'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    @property
    def get_postion(self):
        """会员对应的车位id"""
        postion = self.carpostion_set.first()
        return postion if postion else None


class CarPostion(models.Model):
    member = models.ForeignKey('Member', verbose_name='会员ID', null=True, blank=True, default=None)
    is_member = models.BooleanField('会员位', default=False)
    is_valid = models.BooleanField('可用状态', default=True)
    plate_number = models.CharField('车牌号', max_length=32, null=True, blank=True, default='')
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = 'car_postion'
        verbose_name = 'car_postion'
        verbose_name_plural = verbose_name


class MemberAmount(models.Model):
    member = models.ForeignKey('Member', verbose_name='会员ID', null=True, blank=True)
    money = models.FloatField('金额', default=300.00)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'member_amount'
        verbose_name = 'member_amount'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class TempAmount(models.Model):
    enter_time = models.DateTimeField('进入时间', null=True, blank=True, auto_now_add=True)
    leave_time = models.DateTimeField('离开时间', null=True, blank=True, default=None)
    time_duration = models.FloatField('时长', null=True, blank=True, default=0.0)
    plate_number = models.CharField('车牌号', max_length=32, null=True, blank=True, default='')
    is_member = models.BooleanField('会员', default=False)
    postion = models.ForeignKey('CarPostion', verbose_name='停车位', null=True, blank=True, default=None)
    money = models.FloatField('金额', null=True, blank=True, default=0.0)
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    creator = models.ForeignKey(User, null=True, blank=True, default=None)

    class Meta:
        db_table = 'temp_amount'
        verbose_name = 'temp_amount'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
