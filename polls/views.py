from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Vote, User
from .forms import PollForm

# Create your views here.

@login_required
def index_view(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    vote_by_request_user = Vote.objects.all().filter(
        user=request.user.username).order_by('-vote_time')[:5]

    return render(request, 'polls/index.html', {
        'latest_question_list' : latest_question_list,
        'vote_by_request_user' : vote_by_request_user,
        })

@login_required
def add_poll(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PollForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            try:
                Question.objects.get(
                    question_text=form.cleaned_data['question_text'])
            except (KeyError, Question.DoesNotExist):
                new_poll = Question()
                new_poll.question_text = form.cleaned_data['question_text']
                new_poll.pub_date = timezone.now()
                new_poll.save()
                selected_question = Question.objects.get(
                    question_text=form.cleaned_data['question_text'])
                for i in ['choice_text1', 'choice_text2', 'choice_text3']:
                    new_choice = Choice()
                    new_choice.question = selected_question
                    new_choice.choice_text = form.cleaned_data[i]
                    new_choice.save()
                # redirect to a new URL:
                return render(request, 'polls/add_succeed.html')

            form = PollForm()
            return render(request, 'polls/add.html', 
                {'messages':['Your question is already exist!',], 'form':form })
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PollForm()

    return render(request, 'polls/add.html', {'form': form})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        new_vote = Vote()
        new_vote.question = p.question_text
        new_vote.choice = selected_choice
        voter = User.objects.get(pk=request.user.id)
        new_vote.user = voter.username
        new_vote.vote_time = timezone.now()
        new_vote.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
