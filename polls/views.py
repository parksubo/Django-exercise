from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question


# 템플릿을 로드하고 컨텍스트를 채우고 httpReponse 렌더링된 템플릿의 결과로 반환하는 것이 일반적
# 이를 'render' 쇼트컷을 이용하여 간단하게 작성 가능
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)
'''
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # __lte는 less than equal로 장고에서 제공되는 필터 조건임
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]



# detail에서는 데이터 객체가 존재하지 않을때 http404 에러를 반환함 try except로 에러를 잡는 것이 일반적
# 이를 'get_object_or_404()' 쇼트컷을 이용하여 간단하게 작성 가능
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



'''
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



# 선택 횟수를 증가시키는 코드는 HttpResponse가 아닌 HttpResponseRedirect을 반환
# reverse는
def vote(request, question_id):
    # request가 GET 방식인 경우 pass하고 POST방식인 경우에만 투표하도록 설정할 수 도 있음
    if request.method == 'GET':
        pass
    elif request.method == 'POST':

        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            # 선택 votes를 1추가하고 저장한다음 결과 페이지를 보여줌
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))