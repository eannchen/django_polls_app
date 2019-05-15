from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Choice, Question


# 顯示一個對象列表
class IndexView(generic.ListView):
    # 預設使用 <app name>/<model name>_list.html 的模板
    template_name = 'polls/index.html'
    # 對於 ListView，自動生成的 context 變量是 question_list。
    # 為了覆蓋這，以 context_object_name 屬性，表示要使用 latest_question_list。
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# 顯示一個特定類型對象的詳細信息
class DetailView(generic.DetailView):
    # 通用視圖需要知道它將作用於哪個模型。 由 model 類別屬性提供。
    # 期望從 URL 中捕獲名為 "pk" 的主鍵值，所以把 urls 的 question_id 改成 pk 。
    # 對於 DetailView，question 變數會自動提供，因為使用 Question Model
    model = Question
    # 預設使用 <app name>/<model name>_detail.html 的模板：polls/question_detail.html
    # 或使用 template_name 類別屬性改變預設。
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# 顯示一個特定類型對象的詳細信息
class ResultsView(generic.DetailView):
    model = Question
    # 也使用 template_name，因為也繼承 DetailView，避免模板也用 polls/question_detail.html
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id, )))
