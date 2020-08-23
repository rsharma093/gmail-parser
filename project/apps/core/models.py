# Create your models here.
import re

from django.db import models
import jsonfield

from lib.custom.models import AbstractModel


class EmailAccount(AbstractModel):
    user = models.EmailField()
    sender = models.EmailField()

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    def __repr__(self):
        return f"{EmailAccount.__name__} <{self.id}, {self.user}>"


class EmailAccountParsedData(AbstractModel):
    account = models.ForeignKey(
        "core.EmailAccount",
        on_delete=models.CASCADE,
        related_name="parsed_data",
    )
    message_id = models.TextField()
    from_email = models.EmailField()
    to_emails = models.TextField()
    cc_emails = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=500)
    body = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    parsed_body_content = jsonfield.JSONField()

    class Meta:
        verbose_name = "Email Parsed Data"
        verbose_name_plural = "Email's Parsed Data"
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    def __repr__(self):
        return f"{EmailAccountParsedData.__name__} <{self.id}, {self.account.user}>"

    def extract_details_from_body(self):
        # Parse Phone
        phone_no_pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        matched = re.findall(phone_no_pattern, self.body)
        if matched:
            phone = matched if len(matched) > 1 else matched[0]
        else:
            phone = None
        self.parsed_body_content["phone"] = phone

        # Parse Email
        email_pattern = r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'
        matched = re.findall(email_pattern, self.body)
        if matched:
            email = matched if len(matched) > 1 else matched[0]
        else:
            email = None
        self.parsed_body_content["email"] = email
        self.save()

