#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    """
    自定义分页
    """

    # 分页查询参数名
    page_query_param = 'page'  # 请求第几页
    page_size_query_param = 'page_size'  # 每页多少条数据

    def get_paginated_response(self, data):
        content = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ])
        return Response({
            'code': 0,
            'msg': '返回列表成功',
            'data': content
        })
