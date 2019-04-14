"""
DRF mixins.
"""
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.viewsets import GenericViewSet


class APIGenericViewSet(GenericViewSet):
    gk_serializer_class = None

    @classmethod
    def serializer_errors_message(cls, errors=None):
        if not errors or not isinstance(errors, ReturnDict):
            return ''

        field_errors, non_field_errors = '', ''
        for k, v in errors.items():
            if 'non_field_errors' == k:
                non_field_errors = ';'.join([item.title() for item in v])
            else:
                field_errors = ';'.join(['{0}: {1}'.format(k, ''.join(v)) for k, v in errors.items()])

        return non_field_errors + '' + field_errors

    def to_response(self, code=0, msg='', data=None):
        """"""
        result = {
            'code': code,
            'msg': msg,
            'data': {}
        }
        if data:
            result.update({'data': data})
        return Response(result, status=HTTP_200_OK)


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'code': 0,
                'msg': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        err_msg = self.serializer_errors_message(serializer.errors)
        return Response({
            'code': -1,
            'msg': err_msg
        })

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        need_all = request.query_params.get('need_all', False)
        if need_all:
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 0,
                'msg': '获取成功',
                'data': serializer.data
            })

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'msg': '获取成功',
            'data': serializer.data
        })


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'msg': '获取成功',
            'data': serializer.data
        })


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({
                'code': 0,
                'msg': '更新成功',
                'data': serializer.data
            })
        err_msg = self.serializer_errors_message(serializer.errors)
        return Response({
            'code': -1,
            'msg': err_msg
        })

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'code': 0,
            'msg': '删除成功',
        })

    def perform_destroy(self, instance):
        instance.delete()


class ModelViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   APIGenericViewSet):
    pass
