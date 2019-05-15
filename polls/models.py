import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    # 不只程式上使用，資料庫也使用此變數名稱當做 Field 名
    question_text = models.CharField(max_length=200)
    # 參數字段字串用於Django管理員站點
    pub_date = models.DateTimeField('date published')

    # 是否在最近一天之內的 pub_date
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # was_published_recently 在 Django 管理員站點的呈現設定
    was_published_recently.admin_order_field = 'pub_date'  # 點擊排序
    was_published_recently.boolean = True  # 以圖型替代 True False
    was_published_recently.short_description = 'Published recently?'  # 替代欄位名

    # 使打印時、Django 管理員站畫面能方便識別
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # 在 SQL Field 預設外鍵名稱多加「_id」，可更改
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # 使打印時、Django 管理員站畫面能方便識別
    def __str__(self):
        return self.choice_text


# Usage:
# Question.objects.all()
# Question.objects.filter(id=1)
# Question.objects.filter(pk=1)\
# Question.objects.filter(question_text__startswith='What')
# Question.objects.get(pub_date__year=timezone.now().year)
# Question.objects.order_by('-pub_date')[5]
# q = Question.objects.get(pk=1)
# q.was_published_recently()
# q.choice_set.all()
# q.choice_set.create(choice_text='The sky', votes=0)
# c = q.choice_set.create(choice_text='Just hacking again', votes=0)
# c.question
# c.delete()