# 学习笔记
## 网页
网页的组成部分
- 结构：HTML
- 表现：CSS
- 行为：JavaScript

HTML的标签
- span：放文字信息
- img：放图片信息
- a：点击的链接

## 如何写爬虫
- 在网页上模拟失败登录，获取登录的HTTP请求
    - Request URL
    - Request Method: POST
    - User-Agent
    - Host 
    - Referer：跳转回 
    - Form Data

爬虫的HTTP请求
Cookie：携带加密过后的用户名和密码信息请求网页
User-Agent：客户端的浏览器信息，用于伪装爬虫客户端


## 异常处理
Traceback -> module ->  Error type
异常也是一个类
异常捕获的过程：
- 异常类把错误信息打包到一个对象
- 该对象会自动查找到调用栈
- 直到运行系统找到明确声明如何处理这些异常的位置
- 所有异常继承自BaseException
- Traceback显示出错位置，显示顺序和异常信息对象传播的方向是相反的

常见异常类型
- LookupError下的IndexError和KeyError
- IOError
- NameError
- TypeError
- AttributeError
- ZeroDivisionError
优化异常输出：import pretty_error


## 自顶向下的程序设计
- 从整体分析一个比较复杂的大问题
- 分析方法可以重用
- 拆分到你能解决的范畴
