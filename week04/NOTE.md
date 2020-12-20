# 学习笔记

## 作业
### 要求
使用 Django 展示豆瓣电影中某个电影的短评和星级等相关信息：
- 要求使用 MySQL 存储短评内容（至少 20 条）以及短评所对应的星级；
- 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；
- （选做）在 Web 界面增加搜索框，根据搜索的关键字展示相关的短评。

### 爬虫
存放在`review_spider`路径下，结果存放的MySQL相关操作包括：
``` SQL
CREATE DATABASE movie_review;
CREATE TABLE IF NOT EXISTS `the_call`(
   `review_id` INT UNSIGNED AUTO_INCREMENT,
   `author` VARCHAR(100) NOT NULL,
   `rate` INT NOT NULL,
   `content` VARCHAR(2048),
   `date` datetime DEFAULT NULL,
   PRIMARY KEY ( `review_id` )
);
```
### 页面展示
存放在`movie_review`路径下

## 学习笔记
### Django特点
- 采用MTV框架
    - 模型(Model)
    - 模版(Template)
    - 视图(Views)
- 强调快速开发和代码复用
- 组件丰富
    - ORM(对象关系映射)映射类来构建数据模型
    - URL支持正则表达式
    - 模版可继承
    - 内置用户认证，提供用户认证和权限功能
    - admin管理系统
    - 内置数据表单、Cache缓存系统、国际化系统


### 如何安装
```
pip3 install --upgrade django==2.2.13
```
```
python3
>>> import django
>>> django.__version__
```
#### 安装后遇到的问题
在 python3 中，改变了连接库，改为了`pymysql`库，使用 `pip install pymysql`进行安装，直接导入即可使用
但是在 Django 中， 连接数据库时使用的是 MySQLdb 库，这在与 python3 的合作中就会报以下错误了
```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
```
>解决方法：在Project中的 __init__.py 文件中添加以下代码即可。
import pymysql
pymysql.install_as_MySQLdb()

### 如何启动
创建Django项目
```
$ django-admin startproject test_project
$ tree test_project/
test_project/
├── manage.py
└── test_project
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 5 files
```
manage.py用于管理项目，test_project/test_project/settings.py是项目的配置文件
创建项目中的应用
```
$ cd test_project
$ python3 manage.py startapp index
$ tree index/
index/
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py

1 directory, 7 files
```
运行命令启动服务
```
$ cd test_project
$ python3 manage.py runserver
$ python3 manage.py runserver 0.0.0.0:8099
```

### 解析`settings.py`等基本配置信息
配置文件包括：
- 项目路径
- 密钥
- 域名访问权限
- App列表
- 静态资源，包括CSS、Javascript等
- 模版文件
- 数据库配置
- 缓存
- 中间件

### 编写 URL 规则，实践带变量的 URL、正则和自定义过滤器功能
当一个用户请求 Django 站点的一个页面：
1. 如果传入 HttpRequest 对象拥有 urlconf 属性（通过中间件设置），它的值将被用来代替
ROOT_URLCONF 设置。
2. Django 加载 URLconf 模块并寻找可用的 urlpatterns，Django 依次匹配每个 URL 模式，在与
请求的 URL 匹配的第一个模式停下来。
3. 一旦有 URL 匹配成功，Djagno 导入并调用相关的视图，视图会获得如下参数：
• 一个 HttpRequest 实例
• 一个或多个位置参数提供
4. 如果没有 URL 被匹配，或者匹配过程中出现了异常，Django 会调用一个适当的错误处理视图

如何找到请求对应的视图文件
```
test_project/settings.py -> test_project/urls.py -> index/urls.py -> index/views.py -> function index
```

### 模块和包
模块：  .py 结尾的 Python 程序 
包： 存放多个模块的目录
`__init__.py` 包运行的初始化文件，可以是空文件

### 让URL支持变量
Django支持对URL设置变量，URL变量类型包括：
- str
- int： path(<int:year>, views.myyear) 
- slug
- uuid
- path

### 探究 VIEW 视图功能和使用
Response 直接返回
Render 将返回的模版封装后再返回

#### Django的快捷函数
- `render()` 将给定的模板与给定的上下⽂字典组合在⼀起，并以渲染的⽂本返回⼀个 HttpResponse 对象。 
- `redirect()` 将⼀个 HttpResponseRedirect 返回到传递的参数的适当URL。
- `get_object_or_404()` 在给定的模型管理器( model manager) 上调⽤ get() ，但它会引发 Http404 ⽽不是 模型的 DoesNotExist 异常。

### 使用 ORM API 掌握对数据表的读写和查询等操作
Model -> Table
创建好应用中models.py之后
```
python manage.py migrate
```
Table -> Model
```
python manage.py inspectdb
python manage.py inspectdb > models.py
```

