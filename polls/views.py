from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q, F

from rest_framework import viewsets
from polls.serializers import UserSerializer, GroupSerializer
from polls.models import Choice, Question



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
    return HttpResponse("You're voting on question %s." % question_id)


# Rest tutorial

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



# Answers to the questions in the document. 

def get_all_questions(request):
    return Question.objects.all()

def get_questions_contain_hello(request):
    return Question.objects.filter(question_text__contains='Hello')

def get_questions_NOT_contain_hello(request):
    return Question.objects.exclude(question_text__contains='Hello')

def get_questions_starts_with_h(request):
    return Question.objects.filter(question_text__startswith='h')

def get_questions_newer_than_today(request):
    return Question.objects.filter(question_text__gt=timezone.now())

def get_choices_by_question_text_hello(request):
    return Choice.objects.filter(question__question_text__exact="Hello")

def get_questions_contains_hello_OR_newer_than_today(request):
    return Question.objects.filter(
        Q(question_text="Hello") | Q(pub_date__lt=timezone.now())
    )

def get_choices_with_question_contains_hello_OR_newer_than_today(request):
    return Choice.objects.filter(
        Q(question__question_text="Hello") | Q(question__pub_date__lt=timezone.now())
    )

def get_first_choise_having_3_votes(request):
    return Choice.objects.filter(votes=3).first()

def get_oldest_question(request):
    return Question.objects.order_by('pub_date').first()

def get_number_of_choices_with_hello(request):
    return Choise.objects.filter(choice_text="Hello").count()

def get_post_number_one(request):
    return Post.objects.get(pk=1)

def get_post_where_like_gt_dislikes(request):
    return Post.objects.filter(likes__gt=F('dislikes'))

def update_posts_from_one_like_to_two_likes(request):
    Post.objects.filter(likes=1).update(likes=2)