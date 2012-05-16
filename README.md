# Hanger
## 简单明了的Web框架。

Hanger是基于 [Tornado](http://www.tornadoweb.org/) 以及其它许多代码库的Web微框架。主要是对 Tornado 的扩展和补充，加入了和其他代码库的粘合代码以及一些节省开发时间的功能，并且可以根据需要自己选择是否使用任意一个特性。

框架假定你使用的是 Linux 系统，使用 Nginx 反向代理 Tornado Web Server 。

详细使用方法请自行阅读代码，重点阅读`./hanger/hanger.py`。

框架使用 [WTFPL](http://sam.zoy.org/wtfpl/COPYING) 进行授权。

## 使用

### 安装

    # ./setup.py install

### 示例应用

示例应用中有一个完整的用户注册，登录和设置机制，可以用来参考和引用。

第一次运行示例请创建数据库：

    # python2
    >>> import app
    >>> app.db.create_db()
    # ./runserver.py

## 约定

框架中的约定完全可以不遵守或者修改删除，禁用某个特性只需要在定义继承视图的时候不继承相应的类。

* `AutoTemplatesMixin` 提供一个自动载入和视图类名相同文件名的模板文件的特性。
* `AutoFormsMixin` 能让模板方便的渲染 WTForms 表单，也能让视图方便的验证表单。
* `JinjaMixin` 能让项目使用 Jinja2 模板渲染引擎。
* `BaseHandler` 是一些其他的简单特性，比如方便的json输出。

如果对这些需要更改，请修改 `hanger/hanger.py`的内容。

## 开发

欢迎[前来](https://github.com/tioover/hanger)提交Bug，建议和 Pull Request 。
