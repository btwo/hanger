#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import logging
import traceback

from email.mime.text import MIMEText

class MailMixin(object):
    def send_error_mail(self, template_name, status_code, **kwargs):
        if not self.settings['send_error_mail']:
            return
        exception = "%s\n\n%s" % (kwargs["exception"], traceback.format_exc())
        self.send_mail(
            name = 'errorlog',
            to = self.settings['admin_mail'],
            subject = u"[%s]500 internal server error."\
                % self.settings['site_name'],
            content = self.render_string(template_name, exception=exception))

    def send_mail(self, name, subject, content,
                  to=None, tolist=None, user=None, password=None):
        return send_mail(
            host = self.settings['mail_host'],
            name = name,
            postfix = self.settings['site_domain'],
            tolist = tolist,
            to = to,
            subject = subject,
            content = content,
            user = user,
            password = password,)


def send_mail(host, name, postfix, subject, content,
              to=None, tolist=None, user=None, password=None):
    me = name+"<"+name+"@"+postfix+">"
    msg = MIMEText(content.encode("utf-8"))
    msg.set_charset('utf8')
    msg['Subject'] = subject
    msg['From'] = me
    if not tolist:
        tolist = [to]
    msg['To'] = ";".join(tolist)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(host)
        if user and password:
            smtp.login(user, password) #SMTP
        smtp.sendmail(me, tolist, msg.as_string())
        smtp.close()
        return True
    except Exception, e:
        logging.getLogger().error("%s\n\n%s" % (e, traceback.format_exc()))
        return False
