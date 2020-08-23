# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from lib.custom.custom_filter_backend import FlexFieldsFilterBackend


class FlexFieldsMixin:
    permit_list_expands = []
    _expandable = True
    _force_expand = []

    def list(self, request, *args, **kwargs):
        self._expandable = False
        expand = request.query_params.get("expand")

        if len(self.permit_list_expands) > 0 and expand:
            if expand == "~all":
                self._force_expand = self.permit_list_expands
            else:
                self._force_expand = list(
                    set(expand.split(",")) & set(self.permit_list_expands)
                )

        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        """ Dynamically adds properties to serializer_class from request's GET params. """
        expand = None
        fields = None
        is_valid_request = (
            hasattr(self, "request") and self.request and self.request.method == "GET"
        )

        if not is_valid_request:
            return self.serializer_class

        fields = self.request.query_params.get("fields")
        if not fields and hasattr(self, "fields"):
            fields = self.fields
        fields = fields.split(",") if fields else None

        if self._expandable:
            expand = self.request.query_params.get("expand")
            if not expand and hasattr(self, "expand"):
                expand = self.expand
            expand = expand.split(",") if expand else None
        elif len(self._force_expand) > 0:
            expand = self._force_expand
        return type(
            str("DynamicFieldsModelSerializer"),
            (self.serializer_class,),
            {"expand": expand, "include_fields": fields},
        )


class RelationalGenericViewSet(
    FlexFieldsMixin, viewsets.GenericViewSet
):
    filter_backends = (FlexFieldsFilterBackend,)

    def get_queryset(self):
        # assert self.relational_filter is not None, f"'{self.__class__.__name__}' should include " \
        #                                            f"a `relational_filter` attribute"

        assert self.queryset is not None, (
            f"'{self.__class__.__name__}' should either include "
            f"a `queryset` attribute, or override the `get_queryset()` method."
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        filter_kwargs = {}
        if hasattr(self, "relational_filter"):
            for key, value in self.relational_filter.items():
                filter_kwargs.update({key: self.kwargs[value]})
            queryset = queryset.filter(**filter_kwargs)
        return queryset

    def make_request_mutable(self, request):
        if hasattr(request.data, "_mutable"):
            request.data._mutable = True
        if hasattr(request.GET, "_mutable"):
            request.GET._mutable = True


class ListViewSet(ListModelMixin, RelationalGenericViewSet):
    """
    A viewset that provides `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListRetrieveUpdateViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, RelationalGenericViewSet
):
    """
    A viewset that provides `list`, `retrive` and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class CreateViewSet(CreateModelMixin, RelationalGenericViewSet):
    """
    A viewset that provides `create` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateViewSet(CreateModelMixin, ListModelMixin, RelationalGenericViewSet):
    """
    A viewset that provides `create`, `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveViewSet(RetrieveModelMixin, RelationalGenericViewSet):
    """
    A viewset that provides `retrieve` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveUpdateViewSet(
    RetrieveModelMixin, UpdateModelMixin, RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveDestroyViewSet(
    RetrieveModelMixin, DestroyModelMixin, RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveUpdateDestroyViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveUpdateDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RelationalGenericViewSet,
):
    def get_serializer_context(self):
        return {"request": self.request}

    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListRetrieveViewSet(ListModelMixin, RetrieveModelMixin, RelationalGenericViewSet):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveUpdateViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    RelationalGenericViewSet,
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    RelationalGenericViewSet,
):
    """
    A viewset that provides `retrieve`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass
