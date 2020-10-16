from django.http import HttpResponseRedirect
from polls.models import Questions, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Questions.objects.filter(
                puplished_date__lte=timezone.now()
                ).order_by('puplished_date')[0:5]


class DetailedView(generic.DetailView):
    model = Questions
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Questions.objects.filter(puplished_date__lte=timezone.now())


class Result(generic.DetailView):
    model = Questions
    template_name = 'polls/results.html'


def votes(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, ' polls/detail.html', {
           'question': question,
           'error_message': " you didn't select a choice ",
        })

    else:
        selected_choice.vote_tally += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
