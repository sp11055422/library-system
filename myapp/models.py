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
   priority = models.IntegerField(default=1)    
   open_use = models.BooleanField(default=True) 

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
    device_type = models.CharField(max_length=20)
    assigned_cart = models.ForeignKey(devicecars,on_delete=models.SET_NULL, null=True, blank=True)
    sign_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.teacher_name} - {self.assigned_cart}"

