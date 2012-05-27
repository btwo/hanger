#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def send_mail(host, name, postfix, tolist, subject, content,
              user=None, password=None):
    me = name+"<"+name+"@"+postfix+">"
    msg = MIMEText(content)
    msg.set_charset('utf8')
    msg['Subject'] = subject
    msg['From'] = me
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
        print str(e)
        return False
