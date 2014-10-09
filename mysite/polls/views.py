# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from polls.models import Choice, Poll

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

class PollCreationView(generic.TemplateView):
    template_name = 'polls/poll_creation.html'

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    today = datetime.datetime.now()
    return render(request, 'polls/detail.html', {'poll': poll}) 

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def submit_poll(request):
    question = request.POST['question']
    number = int(request.POST['num_choices'])
    end_date = request.POST['end_date']
    errors = []
    if not question or not number:
        if not question:
            errors.append("You didn't put a question")
        if not number:
            errors.append("You didn't specify a number of options")
        if not end_date:
            errors.append("You didn't specify an end date for the poll")
        return render(request, 'polls/poll_creation.html', {
            'error_message': errors
            })
    else:
        poll = Poll()
        poll.question=question
        poll.pub_date=timezone.now()
        poll.start_date=timezone.now()
        poll.end_date=end_date
        poll.save()
        return HttpResponseRedirect(reverse('polls:option_creation', args=(number, poll.id)))

def create_options(request, number, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render(request, "polls/option_creation.html", {
        'poll': p,
        'number': range(0,int(number))
        })

def submit_options(request):
    options = dict(request.POST)['option']
    poll_id = request.POST['poll_id']
    p = get_object_or_404(Poll, pk=int(poll_id))
    if isinstance(options, basestring):
        opt = Choice()
        opt.poll=p
        opt.choice_text=options
        opt.votes=0
        opt.save()
    else:
        for opt in options:
            c = Choice()
            c.poll = p
            c.choice_text=opt
            c.votes=0
            c.save()
    return HttpResponseRedirect(reverse('polls:index'))
