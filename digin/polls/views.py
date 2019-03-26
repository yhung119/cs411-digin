from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


from django.forms.formsets import formset_factory





class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
	print("vote")
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
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
		
def addChoice(request,question_id):
	print("choice")
	current_user=request.user
	print(current_user.id)
	question = get_object_or_404(Question, pk=question_id)
	inp_value = request.GET.get('choice')
	question = get_object_or_404(Question, pk=question_id)
	question.choice_set.create(choice_text=inp_value,votes=0,userID=request.user.id)
	return HttpResponseRedirect(reverse('polls:vote', args=(question.id,)))
	
def addQuestion(request):
	print("question")
	inp_value = request.GET.get('choice')
	print(request.user.id)
	q=Question(question_text=inp_value,pub_date=timezone.now(),userID=request.user.id)
	q.save()
	return HttpResponseRedirect(reverse('polls:index'))