# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "SERVICE_UNAVAILABLE"


class BadRequest(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "BAD_REQUEST"


class SomethingWrong(APIException):
    status_code = 503
    default_detail = "Something went wrong. please try after some time"
    default_code = "SOMETHING_WENT_WRONG"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
        if response.data.get("detail") and not response.data.get("message"):
            response.data["message"] = response.data["detail"]
            del response.data["detail"]

    return response
