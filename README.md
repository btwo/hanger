# Hanger
## 简单明了的Web框架。

Hanger是基于 [Tornado](http://www.tornadoweb.org/) 以及其它许多代码库的Web微框架。

有一些常用的功能和结构能节省开发时间，并且能迅速的修改，增删修改功能。

使用 [WTFPL](http://sam.zoy.org/wtfpl/COPYING) 进行授权。

## 使用

框架假定你使用的是 Linux 系统，使用 Nginx 反向代理 Tornado Web Server 。

详细使用方法请自行阅读代码，重点阅读`./lib/base.py`。

## 分支

目前项目按照功能不同分为下面一些分支。

* **master**: 主要分支，内置有基本的用户注册登录功能。
* **lite**: 在 master 的基础上删除了用户注册登录功能。

## 依赖

* [Tornado](http://www.tornadoweb.org/)
* [WTForms](http://wtforms.simplecodes.com/docs/dev/)
* [Jinja2](http://jinja.pocoo.org/docs/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [Python Image library(PIL)](http://www.pythonware.com/products/pil/)

## 开发

欢迎[前来](https://github.com/tioover/hanger)提交Bug，建议和 Pull Request 。
