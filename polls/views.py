from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Question


# 템플릿을 로드하고 컨텍스트를 채우고 httpReponse 렌더링된 템플릿의 결과로 반환하는 것이 일반적
# 이를 'render' 쇼트컷을 이용하여 간단하게 작성 가능
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)


# detail에서는 데이터 객체가 존재하지 않을때 http404 에러를 반환함 try except로 에러를 잡는 것이 일반적
# 이를 'get_object_or_404()' 쇼트컷을 이용하여 간단하게 작성 가능
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)