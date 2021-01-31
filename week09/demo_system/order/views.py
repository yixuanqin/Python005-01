from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from order.serializers import UserSerializer, GroupSerializer, OrderInfoSerializer
from order.models import OrderInfo
from order.permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that manage order
    """
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer  # 添加序列化
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 用户必须登录才能访问
    
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = OrderInfoSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    @action(detail = True, methods = ['GET'])
    def cancel(self, request, pk):
        order = OrderInfo.objects.get(id = pk)
        order.order_status = "TRADE_CLOSED"
        order.save()
        serializer = OrderInfoSerializer(order, context={'request': request})
        return Response(serializer.data)