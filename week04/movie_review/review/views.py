from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import TheCall

# Create your views here.
def default(request):
    queryset = TheCall.objects
    condtion = Q(rate__gt = 3)
    review_queryset = queryset.filter(condtion)
    return render(request, 'the_call.html', locals())

def search(request):
    key_word = request.GET.get('q')
    if key_word:
        key_word = key_word.strip()
        queryset = TheCall.objects
        condition1 = Q(rate__gt = 3)
        condition2 = Q(content__icontains = key_word) | Q(author__icontains = key_word) | Q(rate__icontains = key_word)
        review_queryset = queryset.filter(condition1 & condition2)
    else:
        review_queryset = []
    return render(request, 'search_result.html', locals())