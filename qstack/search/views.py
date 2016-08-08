from django.template import RequestContext
from django.shortcuts import render_to_response

from search.forms import SearchForm
from search.utils import AnswerEngine
# Create your views here.


def home(request):
    """
    home for search page
    """
    template = 'search.html'
    search_form = SearchForm()
    ctx = {'search_form': search_form}
    ctx = RequestContext(request, ctx)
    response = render_to_response(template, ctx)
    return response


def process_search(request):
    """
    view for search process
    """
    template = 'search.html'
    search_form = SearchForm(request.GET)
    answer = ''
    if search_form.is_valid():
        answer = AnswerEngine(search_form['query'].value()).get_answer()
        if not answer:
            answer = 'NO answer found.'

    ctx = {'search_form': search_form,
           'answer': answer}
    ctx = RequestContext(request, ctx)
    response = render_to_response(template, ctx)
    return response
