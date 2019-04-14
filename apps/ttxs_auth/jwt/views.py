#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import UserLoginSerializer, \
    UserSignupSerializer, UserLogoutSerializer


class SignupView(viewsets.ModelViewSet):
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        用户注册
        """
        return super(SignupView, self).create(request, *args, **kwargs)


class ConfirmEmailView(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        pass


class LoginView(ObtainJSONWebToken):
    """
        用户jwt方式登录, 获取 token

        根据传入的用户名和密码,为当前用户生成一个合法 token, 该token 值可用于访问当前平台的所有接口
        """
    pass


class LogoutView(viewsets.ModelViewSet):
    serializer_class = UserLogoutSerializer

    def create(self, request, *args, **kwargs):
        """
        用户cookie方式退出登录
        """
        logout(request)
        return Response({'status': 'ok', 'message': '退出成功！'})
