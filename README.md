# Django Api Server Template

这是一个使用 Django 来做 Api Server 的项目模板，方便在开发新项目时快速的创建项目框架。

## 依赖：

- 使用 [Django restframework](https://github.com/encode/django-rest-framework) 集成
- 使用 [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt) 来进行 Jwt 认证
- 使用 [drf-yasg](https://github.com/axnsan12/drf-yasg/) 来提供 Swagger 文档的支持

## 一件改名脚本使用

通过根目录中 rename.py 文件，可以通过以下脚本方面的修改为新的项目名称，至于根目录的文件名，你可以随意更改。

```shell
# 例如我要修改名称为 new_project_name
python3 ./rename.py new_project_name
```
这个过程将 django 工程目录中的如下四个文件中的文件字符做替换，为了方便校验保存了备份文件：
- django_api_server_template/wsgi.py
- django_api_server_template/asgi.py
- settings/base.py
- manage.py

同时也修改了 django 工程目录名。

## 开发进度：

- [x] Django restframework 集成
- [x] djangorestframework-simplejwt 集成
- [x] drf-yasg 集成
- [ ] RequestId 中间件
- [x] 请求时间中间件
- [ ] 密码传输非对称加密
- [x] 一键改名脚本
- [x] Admin example
- [ ] 增加部署文件


# Reference:
- https://github.com/juhanakristian/django-rename