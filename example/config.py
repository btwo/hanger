# coding=utf-8
from os.path import join
from example import PATH, ui

settings = dict(
    # general
    site_name = u'YourSiteName',
    site_domain = 'your.url',
    debug = True,
    ui_methods = ui,
    port = 8888,
    login_url = '/signin/',
    # Security
    xsrf_cookies = True,
    cookie_secret = r'哈哈你看看你!!',
    # path
    template_path = join(PATH, 'templates'),
    static_path = join(PATH, 'static'),
    logfile_path = join(PATH, 'error.log'),
    # email
    send_error_mail = True,
    admin_mail = 'tioover@gmail.com',
    mail_host = '127.1',
)
settings['mail_postfix'] = settings['site_domain']
settings['avatar_path'] = join(settings['static_path'], 'avatar')
