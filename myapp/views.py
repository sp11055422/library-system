from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from .models import Reservation

@csrf_exempt
def google_form_webhook(request):
    if request.method == 'POST':
        try:
            # 1. 接收從 Google 表單傳過來的 JSON 資料
            data = json.loads(request.body.decode('utf-8'))
            
            # 2. 提取欄位資料（這些名稱要請負責 Google 端的人對齊）
            teacher_name = data.get('teacher_name')
            target_class = data.get('target_class')
            class_size   = int(data.get('class_size', 0))
            date_str     = data.get('date')
            period       = data.get('period')
            device_type  = data.get('device_type')
            
            # 3. 轉換日期格式並建立預約單
            parsed_date = parse_date(date_str)
            reservation = Reservation(
                teacher_name=teacher_name,
                target_class=target_class,
                class_size=class_size,
                date=parsed_date,
                period=period,
                device_type=device_type
            )
            # 4. 存檔（這會直接觸發你之前寫好的自動分配車子大腦）
            reservation.save()

            return JsonResponse({'status': 'success', 'message': '資料已成功寫入資料庫並分配車輛'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': '必須使用 POST 方法'}, status=405)
