import datetime
import json
import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import AllowProject, BluetoothPassword

# 生成密码的字符集
CHARS = "0123456789ABCDEF"
# 流水号
serial_number = 10000
# 周
weekend = 1


# 生成随机密码
def get_password():
    global CHARS
    chars = [random.choice(CHARS) for i in range(24)]
    password = ''.join(chars)
    return password


@require_GET
def index(request):
    series = AllowProject.objects.all()
    context = {
        "series": series
    }
    return render(request, 'index.html', context)


@require_POST
def add_name(request):
    name = request.POST.get("name")
    if not name:
        return JsonResponse({"code": 400, "msg": "产品名不能为空"})
    name = name.strip()
    if len(name) == 0:    # 输入空格
        return JsonResponse({"code": 400, "msg": "产品名不能为空"})
    if len(name) != 4:
        return JsonResponse({"code": 400, "msg": "产品名长度不规范"})
    exists = AllowProject.objects.filter(series_name=name)
    if exists:
        return JsonResponse({"code": 400, "msg": "该产品名称已存在"})
    AllowProject.objects.create(series_name=name)
    return JsonResponse({"code": 200, "msg": "添加成功"})


@ require_POST
def remove(request):
    name_id = request.POST.get('id')
    if not name_id:
        return JsonResponse({"code": 400, "msg": "id不能为空"})
    try:
        AllowProject.objects.get(pk=name_id).delete()
    except AllowProject.DoesNotExist:
        return JsonResponse({"code": 400, "msg": "该数据不存在"})
    return JsonResponse({"code": 200, "msg": "删除成功"})


@csrf_exempt
@require_POST
def create_sn(request):
    try:
        receive_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"code": 401, "msg": "json格式错误", "data": None})
    series = receive_data.get('series')
    barcode = receive_data.get('barcode')
    exits = AllowProject.objects.filter(series_name=series).exists()
    if not exits:
        return JsonResponse({"code": 403, "msg": "该系列产品不允许生产", "data": None})
    year, weekday, day = datetime.datetime.now().isocalendar()
    global weekend
    global serial_number
    # 当周发送变化时，修改周信息和起始流水号
    if weekday != weekend:
        serial_number = 10000
        weekend = weekday
    sn_head = series + str(year)[2:] + str(weekday)
    if serial_number == 10000:     # 可能是程序重启或者下一周
        sn_exits = BluetoothPassword.objects.filter(sn__startswith=sn_head).exists()
        if sn_exits:
            last_sn = BluetoothPassword.objects.filter(sn__startswith=sn_head).order_by("create_time").last()
            serial_number = int(last_sn.sn[-5:])
    serial_number += 1
    sn = sn_head + str(serial_number)
    password = get_password()
    record = BluetoothPassword(sn=sn, password=password, barcode=barcode)
    record.save()
    response_data = {
        "code": 200,
        "message": "成功",
        "data": {
            "barcode": barcode,
            "password": password,
            "sn": sn,
            "create_time": record.create_time
        }
    }
    return JsonResponse(response_data)
