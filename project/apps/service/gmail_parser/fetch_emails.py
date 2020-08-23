# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import email
import imaplib

from lib.custom.exceptions import BadRequest
import datetime
import re


class ParseGmail:
    def __init__(self, user, password, sender):
        self.user = user
        self.password = password
        self.sender = sender
        self.con = None

    # Function to get email content part i.e its body part
    def get_body(self, msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)

    # Function to search for a key value pair
    def search(self, key, value):
        result, data = self.con.search(None, key, '"{}"'.format(value))
        return data

    # Function to parse email
    def parse_emails(self, text):
        if text is None:
            return None
        email_pattern = r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'
        matched = re.findall(email_pattern, text)
        if matched:
            return ",".join(matched) if len(matched) > 1 else matched[0]
        return None

    def parse(self):
        try:
            # Create our connection to our Gmail account
            self.con = imaplib.IMAP4_SSL("imap.gmail.com")
            self.con.login(self.user, self.password)
            self.con.select('inbox')

            # Search through our selected folder
            data = self.search("FROM", self.sender)
            mail_ids = data[0]

            # Count our emails
            id_list = mail_ids.split()
            parsed_data = []
            # iterate through each of our counted emails
            for i in id_list[::-1]:
                result, data = self.con.fetch(i, '(RFC822)')
                for response_part in data:
                    try:
                        # Load our captured email data into variables
                        msg = email.message_from_bytes(response_part[1])
                        date = msg.get("Date")
                        if date:
                            date = datetime.datetime.strptime(msg.get("Date").split("+")[0].strip(), '%a, %d %b %Y %H:%M:%S')
                        print(msg.items())
                        email_data = {
                            "subject": msg.get('Subject'),
                            "from_email": self.parse_emails(msg.get('From')),
                            "to_emails": self.parse_emails(msg.get('To')),
                            "date": date,
                            "body": self.get_body(msg).decode("utf-8"),
                            "cc_emails": self.parse_emails(msg.get("Cc")),
                            "message_id": msg.get("Message-ID")
                        }
                        parsed_data.append(email_data)

                    except Exception as e:
                        pass

            return parsed_data
        except Exception as e:
            raise BadRequest({"error": str(e)})

        # Close our selected folder and logout
        finally:
            if self.con is not None:
                self.con.close()
                self.con.logout()
