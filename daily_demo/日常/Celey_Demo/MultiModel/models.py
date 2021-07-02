from django.db import models


# Create your models here.
class Teachers(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.BooleanField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'teachers'


class Students(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.BooleanField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)  # 默认自动关联其他表的主键

    class Meta:
        db_table = 'students'
