from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from django.utils import timezone


from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
# from django.template import loader

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions"""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ','.join([q.Question.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }

    # return HttpResponse(output)
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # return HttpResponse("You are looking at question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})


def results(request, question_id):
    response = "You are looking at the result of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You are voting on question %s. " % question_id)
"""


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(question.question_text)
    pprint(request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print("TRY")
        # print(selected_choice)
        # except (KeyError, ObjectDoesNotExist):
    except (KeyError, Choice.DoesNotExist):
        print("ERROR :")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        print("ELSE")
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# Create your views here.
