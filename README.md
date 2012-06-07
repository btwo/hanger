# Hanger
## 简单明了的Web框架。

Hanger是基于 [Tornado](http://www.tornadoweb.org/) 以及其它许多代码库的Web微框架。主要是对 Tornado 的扩展和补充，加入了和其他代码库的粘合代码以及一些节省开发时间的功能，并且可以根据需要自己选择是否使用任意一个特性。

框架假定你使用的是 Linux 系统，使用 Nginx 反向代理 Tornado Web Server 。

详细使用方法请自行阅读代码，重点阅读`./hanger/hanger.py`。

框架使用 [WTFPL](http://sam.zoy.org/wtfpl/COPYING) 进行授权。

## 安装

    # ./setup.py install

## 示例应用

示例应用中有一个完整的用户注册，登录和设置机制，可以用来参考和引用。

### 运行示例

    # cd example
    # ./server.py

### 示例应用的配置

配置文件在 `example/conf/` 中，包含了应用本身的配置文件 `config.json` ，和 Nginx 配置文件 `proxy.conf`，Redis键值数据库配置文件 `redis.conf` 。以及启动服务器和相关进程的守护进程管理程序配置文件 `supervisord.conf`。

## 开始你的项目

你可以选择参照 `./example` 中的示例项目自己从头开始创建一个项目。

或者可以编辑 `./example/config.py` 配置文件后运行 `./example/project_init.py` 来开始你的项目。

并且将 `example` 文件夹重命名成你的项目名称和移动到它应该在的位置。

如果示例项目有任何难懂的地方，可以在[项目主页提交一个 Issue](https://github.com/tioover/hanger/issues)。

### 部署
依赖的外部程序为Nginx，Redis以及Supervisor。

1. 使用 `./example/project_init.py` 通过你的项目配置文件来配置其他组件。
2. 将Nginx配置 `proxy.conf` 复制到配置目录，重启Nginx启用。
3. 启动 Supervisord `supervisord -c <your_application_path>/conf/supervisord.conf`

## 特性

框架中的约定完全可以不遵守或者修改删除，禁用某个特性只需要在定义继承视图的时候不继承相应的类。

* `BaseHandler` 继承`tornado.web.RequestHandler`，是最基本的，在多重继承列表中必须填到最后面以便其他类能正常工作，另外有一些其他的简单特性，比如方便的json输出。
* `JinjaMixin` 能让项目使用 Jinja2 模板渲染引擎。
* `AutoTemplatesMixin` 提供一个自动载入和视图类名相同文件名的模板文件的特性。
* `AutoFormsMixin` 能让模板方便的渲染 WTForms 表单，也能让视图方便的验证表单。
* `MailMixin` 邮件发送特性，`MailMixin.send_mail`方法可以用来发送邮件，继承这个 Class 后如果服务器遇到 500 错误，会自动发送错误信息给你的邮箱。

如果对这些需要更改，请修改 `./hanger/`文件夹中的内容。

## 开发

欢迎[前来](https://github.com/tioover/hanger)提交Bug，建议和 Pull Request 。
