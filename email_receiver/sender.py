import os

from smtplib import SMTP_SSL


class Email:
    def __init__(self):
        self._from = os.environ.get('EMAIL_FROM')
        self.server = os.environ.get('EMAIL_SERVER')
        self.pwd = os.environ.get('EMAIL_PWD')

        if not self._from:
            raise ValueError('Email from is required!')

        if not self.server:
            raise ValueError('Email server is required!')

        if not self.server:
            raise ValueError('Email password is required!')

    def sendemail(self, to, subject, msg):
        smtp_client = SMTP_SSL(self.server, 465)
        smtp_client.login(self._from, self.pwd)
        _msg = "\r\n".join([
            "From: {0}".format(self._from),
            "Subject: {0}".format(subject),
            "{0}".format(msg),
        ])

        resp = smtp_client.sendmail(self._from, to, _msg)

        smtp_client.close()

        return resp
