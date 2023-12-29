from django.http import HttpResponse
from django.shortcuts import render


from .models import Question
from django.http import Http404
from django.shortcuts import get_object_or_404


def index(request):
    '''Simple function based view.'''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    '''Detail view for qiven question'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    '''Results of the given question'''
    response = f"You're looking at question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")