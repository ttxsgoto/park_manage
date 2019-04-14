#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.contrib.auth import hashers
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserSignupSerializer(serializers.ModelSerializer):
    """
    用户注册
    """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data['password'])
        return super(UserSignupSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    用户登录
    """

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    """
    退出登录
    """

    class Meta:
        model = User
        fields = ()


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    修改密码
    """

    old_password = serializers.CharField(label='旧密码')
    new_password = serializers.CharField(source='password', label='新密码')

    class Meta:
        model = User
        fields = ('old_password', 'new_password')


class AuthorizationTokenSerializer(serializers.Serializer):
    account = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        required=True,
        view_name='api:account-detail',
    )

    class Meta:
        fields = ['account']
