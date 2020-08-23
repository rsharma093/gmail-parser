# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models


class _DateTimeStampingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractModel(_DateTimeStampingModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
