from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class OrderInfo(models.Model):
    ORDER_STATUS = (
        ('PENDING_PAYMENT', '等待支付'),
        ('COMPLETED_PAYMENT', '完成支付'),
        ('TRADE_CLOSED', '关闭订单'),
        ('TRADE_COMPLETED', '完成订单')
    )
    user = models.ForeignKey(User, verbose_name = '下单用户', help_text = '下单用户', on_delete = models.CASCADE)
    order_id = models.CharField(max_length = 30, unique = True, blank = True, null = True, verbose_name = '订单号', help_text = '订单号')
    order_status = models.CharField(choices = ORDER_STATUS, default = 'PENDING_PAYMENT', max_length = 20, verbose_name = '订单状态', help_text = '订单状态')
    order_amount = models.FloatField(default = 0.0, verbose_name = '订单金额', help_text = '订单金额')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = '下单时间')
    modified_time = models.DateTimeField(auto_now = True, verbose_name = '下单时间')
  
    class Meta:
        verbose_name_plural = verbose_name = '订单'
        ordering = ['-created_time']

    def __str__(self):
        return "{}".format(self.order_id)
