# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import six
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework import exceptions
from rest_framework.views import set_rollback
from rest_framework.response import Response


class PermissionFORBIDDEN(exceptions.APIException):
    """权限禁止"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('无权限访问')
    default_code = 'permission_forbidden'


def custom_exception_handler(exc, context):
    """
    异常处理handler.
    """

    if isinstance(exc, Http404):
        msg = _('对应资源不存在.')
        data = {
            'code': -1,
            'msg': six.text_type(msg),
            # 'content': exc.default_content
        }
        set_rollback()
        return Response(data, status=200)

    elif isinstance(exc, PermissionDenied):
        msg = _('无权限访问.')
        data = {
            'code': -1,
            'msg': six.text_type(msg),
            # 'content': exc.default_content
        }
        set_rollback()
        return Response(data, status=200)
    elif isinstance(exc, exceptions.NotAuthenticated):
        msg = _('您的登录已过期，请重新登录！')
        data = {
            'code': -1,
            'msg': six.text_type(msg),
            # 'content': exc.default_content
        }

        set_rollback()
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, exceptions.AuthenticationFailed):
        msg = _('用户未认证，请登录！')
        data = {
            'code': -1,
            'msg': six.text_type(msg)
        }
        set_rollback()
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        field_name = ''
        if isinstance(exc.detail, dict):
            field_name = next(iter(exc.detail.keys()))
            detail = exc.detail[field_name][0] if isinstance(exc.detail[field_name], list) else exc.detail[field_name]
            data = {
                # 'code': exc.code if hasattr(exc, 'code') else exc.status_code,
                'code': exc.code if hasattr(exc, 'code') else -1,
                'msg': exc.msg if hasattr(exc, 'msg') else detail,
                'field_name': field_name
            }
        elif isinstance(exc.detail, list):
            detail = exc.detail[0]
            data = {
                'code': exc.code if hasattr(exc, 'code') else exc.status_code,
                'msg': exc.msg if hasattr(exc, 'msg') else detail,
                'field_name': field_name
            }
        else:
            msg = exc.detail
            if exc.detail == '无效页面。':
                msg = six.text_type(_('没有更多资源了'))
            data = {
                'code': -1,  # int('10{status_code}'.format(status_code=exc.status_code)),
                'msg': msg,
            }

        set_rollback()
        return Response(data, status=200, headers=headers)

    return None
