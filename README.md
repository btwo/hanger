# Hanger
## 简单明了的Web框架。

一个基于[Tornado](http://www.tornadoweb.org/)以及其它许多代码库的Web微框架。

有一些常用的功能和结构能节省开发时间，并且能迅速的修改，增删修改功能。

使用 [WTFPL](http://sam.zoy.org/wtfpl/COPYING) 进行授权。

## ToDo

* 可以让用户自行选择是否带有附加功能，如用户登录注册。
* Redis 支持
* 使用 Redis 储存session。
* Email 找回密码。
* Nginx 文件上传模块支持。
* 使用 sqlalchemy ORM

## 使用

假定你使用的是Linux系统，使用Nginx反向代理Tornado Web Server。

详细请自行阅读代码，这里有一份[简单的使用指南](https://github.com/tioover/hanger/wiki)。

## 安装需求

* Python 2.7
* [Tornado](http://www.tornadoweb.org/)
* [WTForms](http://wtforms.simplecodes.com/docs/dev/)
* [Jinja2](http://jinja.pocoo.org/docs/)
* [Markdown2](https://github.com/trentm/python-markdown2)
* [Elixir](http://elixir.ematia.de/trac/wiki)
* [Python Image library(PIL)](http://www.pythonware.com/products/pil/)
