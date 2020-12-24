from django.db import models
from login import models as login_models

# Create your models here.
class Person(models.Model):
    user = models.ForeignKey(to=login_models.User,on_delete=models.CASCADE)  # 用户
    name = models.CharField(max_length=10)  # 患者姓名
    age = models.CharField(max_length=5)  # 年龄
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    sex = models.CharField(max_length=32, choices=gender, default="男")  # 性别
    phone = models.CharField(max_length=11)  # APP登录账号
    password = models.CharField(max_length=256)  # 登录密码
    creat_time = models.DateTimeField(auto_now_add=True)  # 创造时间

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-creat_time"]
        verbose_name = "患者"
        verbose_name_plural = "患者"

class EcgData(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)  # 患者
    record_begin_time = models.DateField(auto_now=True)  # ECG记录的日期
    ecg_time = models.CharField(max_length=128)  # 记录时长
    ecg_path = models.TextField()  # ECG存储路径
    ecg_hz = models.CharField(max_length=128)  # 采样率
    # upload_time = models.DateTimeField(auto_now_add=True)  #上传时间
    ecg_img = models.TextField()  #心电图存储路径
    ecg_result = models.TextField()  # 模型预测结果

