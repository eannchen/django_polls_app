from django.contrib import admin
from .models import Question, Choice

# 註冊 Model，始可在 Django 管理員站點管理
# admin.site.register(Question)
# admin.site.register(Choice)

# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # 清單顯示時，要呈現的欄位
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # 清單顯示時，過濾選項(pub_date欄位依照 DateTimeField，Django 知道要用哪種Filter)
    list_filter = ['pub_date']

    # 搜尋功能，可搜尋 question_text 欄位，使用 LIKE 查詢
    search_fields = ['question_text']

    # 分頁，每頁顯示幾筆資料
    list_per_page = 100

    #  編輯欄位呈現方式
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {
            'fields': ['question_text']
        }),
        ('Date information', {
            'fields': ['pub_date']
        }),
    ]
    # 添加三個關聯
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
