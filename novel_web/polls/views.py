from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
#from django.http import HttpResponse
from .models import Question,Choice
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#from django.template import loader
class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    model=Question
    template_name="polls/Detail.html"
class ResultsView(generic.DetailView):
    model=Question
    template_name = "polls/resutls.html"
def index(request):
    latest_quesiton_list=Question.objects.order_by('-pub_date')[:5]
    context={'latest_question_list':latest_quesiton_list,}
    return render(request,'polls/index.html',context)

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))
#reverse:the view function passed the control and the arguments

