# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from rest_framework.pagination import PageNumberPagination


class NoPagination(PageNumberPagination):
    page_size = sys.maxsize
    max_page_size = sys.maxsize


class Count15Pagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = sys.maxsize
