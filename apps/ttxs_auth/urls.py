#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, unicode_literals
from django.conf.urls import url

from .jwt import views as jwtviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    # jwt
    url('^jwt/signup/$', jwtviews.SignupView.as_view({'post': 'create'})),
    url('^jwt/login/$', jwtviews.LoginView.as_view()),
    # url('^jwt/logout/$', tokenviews.LogoutView.as_view({'post': 'create'})),
    url(r'^jwt/api-token-auth/', obtain_jwt_token),     # 生成jwt
    url(r'^jwt/api-token-refresh/', refresh_jwt_token), # 刷新jwt
    url(r'^jwt/api-token-verify/', verify_jwt_token),   # 返回jwt是否正确,如果正确返回对应的值,如果过期,返回相关信息
]

