from django.db import models


class AllowProject(models.Model):
    series_name = models.CharField("产品系列名称", max_length=10)

    create_time = models.DateTimeField("创建时间", auto_now_add=True)


class BluetoothPassword(models.Model):
    sn = models.CharField("蓝牙SN", max_length=20)
    password = models.CharField("蓝牙密码", max_length=20)
    barcode = models.CharField("条码", max_length=32, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
