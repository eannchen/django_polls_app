from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Question, Choice
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    # render 快捷方法：
    # It returns an HttpResponse object of the given template rendered with the given context.
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # It raises Http404 if the object doesn't exist.
    # .get() or Http404
    question = get_object_or_404(Question, pk=question_id)
    # .filter() or Http404
    # question = get_list_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):  # 字典可能引發的 KeyError，或 get 不到
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse 可帶入別名，回傳 url
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id, )))

        # 這樣處理可能引發 race conditions，兩個線程都取得值，某一線程先更新並儲存，
        # 但另一線程仍用原值去更新儲存。
        # 可以 F() 解決，不需用 .refresh_from_db() 重抓:
        # from django.db.models import F
        # selected_choice.votes = F('votes') + 1
        # selected_choice.save()
