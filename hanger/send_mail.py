#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import logging
import traceback

from email.mime.text import MIMEText

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
