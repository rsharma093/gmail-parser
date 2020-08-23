# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from core.models import EmailAccount, EmailAccountParsedData
from lib.custom.serializers import FlexFieldsModelSerializer


class EmailAccountSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = EmailAccount
        fields = "__all__"

    expandable_fields = {
        "parsed_data": ("core.EmailAccountParsedDataSerializer", {"source": "parsed_data", "many": True})
    }


class EmailAccountParsedDataSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = EmailAccountParsedData
        fields = "__all__"
