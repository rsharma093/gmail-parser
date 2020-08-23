# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from celery_config import celery_app
from core.models import EmailAccountParsedData


@celery_app.task(name="extract_content_from_gmail_task", queue="default_queue")
def extract_content_from_gmail_task(pd_ids):
    for pd_instance in EmailAccountParsedData.objects.filter(id__in=pd_ids):
        pd_instance.extract_details_from_body()
