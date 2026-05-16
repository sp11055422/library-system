from django.db import models

# Create your models here.
class devicecars(models.Model):
   
   category = [
      ('IPAD', 'iPad'),
      ('CHROMEBOOK', 'Chromebook'),
      ('SURFACE', 'Surface Go'),
      ('ACER', 'Acer 小筆電'),
   ]

   car_name = models.CharField(max_length=50)
   category = models.CharField(max_length=20, choices=category)
   priority = models.IntegerField(default=1)  # 優先順序，數字愈小愈先分配 (例如 B=1, D=2, F=3)  
   open_use = models.BooleanField(default=True) # 是否開放使用 (M車可以設為 False)
   def __str__(self):
     return self.car_name


   

   
class Reservation(models.Model):

    periods = [
        ('1', '第1節'), ('2', '第2節'), ('3', '第3節'), ('4', '第4節'),
        ('NOON', '午休'), ('5', '第5節'), ('6', '第6節'), ('7', '第7節'), ('8', '第8節'),
        ('OTHER', '其他'),
    ]

    teacher_name = models.CharField(max_length=50)
    target_class = models.CharField(max_length=20)
    class_size = models.IntegerField()
    date = models.DateField()
    period = models.CharField(max_length=10, choices=periods)
    device_type= models.CharField(max_length=20)
    assigned_cart = models.ForeignKey(devicecars,on_delete=models.SET_NULL, null=True, blank=True)
    sign_time = models.DateTimeField(auto_now_add=True)# 建立時間，用來判斷「先到先得」

    def auto_assign(self):
        # 1. 注意這裡要用 open_use，因為你的截圖裡是用這個名字
        available_carts = devicecars.objects.filter(
            category=self.device_type, 
            open_use=True
        ).order_by('priority')

        # 2. 檢查 Reservation 的篩選 (這部分通常沒問題)
        booked_cart_ids = Reservation.objects.filter(
            date=self.date,
            period=self.period
        ).values_list('assigned_cart', flat=True)
        
        candidate_carts = available_carts.exclude(id__in=booked_cart_ids)

        for cart in candidate_carts:
            # 3. 如果你有寫人數限制，記得檢查規則
            # 如果目前只是要測試成功，可以先註解掉人數限制邏輯
            self.assigned_cart = cart
            return True 
        return False
    
    def save(self, *args, **kwargs):
        # 1. 修正大小寫問題 (避免 ipad 找不到 IPAD)
        if self.device_type: #如果這張預約單上面有填寫設備類型（不是空的）。
            self.device_type = self.device_type.upper()
            
        # 2. 如果這筆預約還沒分配車位，就啟動自動分配
        if not self.assigned_cart:
            self.auto_assign()
            
        # 3. 呼叫原本內建的 save，把資料正式存進資料庫
        super().save(*args, **kwargs)

    
    
    
    
    
    
 

