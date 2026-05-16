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
   priority = models.IntegerField(default=1)  # 優先順序 
   open_use = models.BooleanField(default=True) # 是否開放使用 
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
        
        available_carts = devicecars.objects.filter(
            category=self.device_type, 
            open_use=True
        ).order_by('priority')

        booked_cart_ids = Reservation.objects.filter(
            date=self.date,
            period=self.period
        ).values_list('assigned_cart', flat=True)
        
        candidate_carts = available_carts.exclude(id__in=booked_cart_ids)

        for cart in candidate_carts:
          
            self.assigned_cart = cart
            return True 
        return False
    
    def save(self, *args, **kwargs):
        # 大小寫問題 
        if self.device_type: 
            self.device_type = self.device_type.upper()
            
        # 自動分配
        if not self.assigned_cart:
            self.auto_assign()
            
        # 資料存進資料庫
        super().save(*args, **kwargs)

    
    
    
    
    
    
 

