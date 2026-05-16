from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from .models import Reservation

@csrf_exempt
def google_form(request):
    if request.method == 'POST':
        try:
          
            data = json.loads(request.body.decode('utf-8'))
            teacher_name = data.get('teacher_name')
            target_class = data.get('target_class')
            class_size   = int(data.get('class_size', 0))
            date_str     = data.get('date')
            period       = data.get('period')
            device_type  = data.get('device_type')
            
            
            parsed_date = parse_date(date_str)
            reservation = Reservation(
                teacher_name=teacher_name,
                target_class=target_class,
                class_size=class_size,
                date=parsed_date,
                period=period,
                device_type=device_type
            )
            
            reservation.save()

            return JsonResponse({'狀態': '成功', 'message': '資料已成功寫入資料庫並分配車輛'}, status=200)

        except Exception as e:
            return JsonResponse({'狀態': '有問題', 'message': str(e)}, status=400)

    return JsonResponse({'狀態': '錯誤', 'message': '必須使用 POST 方法'}, status=405)
