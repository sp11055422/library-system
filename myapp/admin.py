from django.contrib import admin
from .models import devicecars, Reservation

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # list_display 就是後台列表會顯示的欄位
    list_display = ('teacher_name', 'target_class', 'class_size', 'date', 'period', 'device_type', 'assigned_cart', 'sign_time')

# 幫 DeviceCart 模型設定後台顯示格式
@admin.register(devicecars)
class DeviceCartAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'category', 'priority', 'open_use')