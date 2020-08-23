# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from core.views import EmailAccountViewSet
from rest_framework.routers import SimpleRouter

core_router = SimpleRouter()
core_router.register("accounts", EmailAccountViewSet, basename="email-account")
urlpatterns = core_router.urls
