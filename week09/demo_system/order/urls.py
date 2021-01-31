
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order import views
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token

# 功能     路径                 方式
# 列出订单  /orders             GET
# 查看订单  /orders/{id}        GET
# 创建订单  /orders/create      POST
# 取消订单  /orders/{id}/cancel UPDATE
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'orders', views.OrderInfoViewSet)  # 订单管理

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('docs',include_docs_urls(title = 'User Manual')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]