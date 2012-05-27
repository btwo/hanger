#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def send_mail(mail_host, mail_user, mail_postfix, to_list, sub, content,
              mail_pass=None):
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg.set_charset('utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host)
        if mail_pass:
            smtp.login(mail_user,mail_pass) #SMTP
        smtp.sendmail(me, to_list, msg.as_string())
        smtp.close()
        return True
    except Exception, e:
        print str(e)
        return False
