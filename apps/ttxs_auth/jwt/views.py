#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, JSONWebTokenAPIView, jwt_response_payload_handler
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


class LoginView(JSONWebTokenAPIView):
    """
        用户jwt方式登录, 获取 token

        根据传入的用户名和密码,为当前用户生成一个合法 token, 该token 值可用于访问当前平台的所有接口
    """
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return Response({
                'code': 0,
                'data': response_data
            })

        return Response({
            'code': 402,
            'msg': serializer.errors,
            'status': status.HTTP_400_BAD_REQUEST})


class LogoutView(viewsets.ModelViewSet):
    serializer_class = UserLogoutSerializer

    def create(self, request, *args, **kwargs):
        """
        用户cookie方式退出登录
        """
        logout(request)
        return Response({'status': 'ok', 'message': '退出成功！'})
