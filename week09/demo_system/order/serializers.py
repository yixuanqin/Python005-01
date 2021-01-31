from django.contrib.auth.models import User, Group
from rest_framework import serializers
from order.models import OrderInfo
import time
from random import randint

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()  # 表示user为隐藏字段，默认为获取当前登录用户
    )
    order_id = serializers.CharField(read_only = True)
    pay_time = serializers.DateTimeField(read_only = True)

    def generate_order_id(self):
        order_id = '{time_stamp}{user_id}{random_int}'.format(
                                                            time_stamp = time.strftime('%Y%m%d%H%M%S'), 
                                                            user_id = self.context['request'].user.id, 
                                                            random_int = randint(10, 99))
        return order_id

    def validate(self, attrs):
        attrs['order_id'] = self.generate_order_id()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"