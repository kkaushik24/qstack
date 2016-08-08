import json
import requests
import urllib
import BeautifulSoup

from search.models import Query, QueryQuestion


class QuestionEngine(object):

    def __init__(self, query, *args, **kwargs):
        super(QuestionEngine, self).__init__(*args, **kwargs)
        self._query = query
        self._base_url = 'https://api.stackexchange.com/2.2/search/advanced'
        self._encoded_query = urllib.urlencode({'q': self._query,
                                                'site':
                                                'stackoverflow',
                                                'accepted': True})
        self._query_url = self._base_url + '?' + self._encoded_query
        self._stackoverflow_response = {}
        self._question_list = None

    def get_response_from_stackoverflow(self):
        response = requests.get(self._query_url)
        self._stackoverflow_response = json.loads(response.content)
        return self._stackoverflow_response

    def index_stackoverflow_response(self):
        query = Query.objects.filter(query=self._query)
        if not query:
            query = Query.objects.create(query=self._query)
            question_items = self._stackoverflow_response.get('items', [])
            self._index_questions(question_items, query.pk)

    def _index_questions(self, question_items, query_id):
        question_list = [QueryQuestion(query_id=query_id,
                         title=question.get('title', ''),
                         stackoverflow_view_count=question.get('view_count',
                                                               0),
                         accepted_answer_id=question.get('accepted_answer_id',
                                                         -1),
                         stackoverflow_answer_count=question.get('answer_couont', 0),
                         stackoverflow_link=question.get('link'),
                         stackoverflow_score_count=question.get('score_count', 0))
                         for question in question_items]
        self._question_list = QueryQuestion.objects.bulk_create(question_list)

    def get_questions(self):
        question_ids = [question.id for question in self._question_list]
        return QueryQuestion.objects.filter(id__in=question_ids)


class AnswerEngine(object):

    def __init__(self, query, *args, **kwargs):
        super(AnswerEngine, self).__init__(*args, **kwargs)
        self._query = query
        self._questions = None

    def _search_local_db(self):
        self._questions = QueryQuestion.objects.filter(query__query__icontains=self._query)

    def _search_stackoverflow(self):
        query_engine = QuestionEngine(self._query)
        query_engine.get_response_from_stackoverflow()
        query_engine.index_stackoverflow_response()
        self._questions = query_engine.get_questions()

    def _rank_questions(self):
        if self._questions:
            self._question = self._questions.order_by('-stackoverflow_view_count')

    def get_answer(self):
        self._search_local_db()
        if not self._questions:
            self._search_stackoverflow()
        self._rank_questions()
        question_for_query = None
        if self._questions:
            question_for_query = self._questions[0]
        answer_html = ''
        if not question_for_query.answer_html:
            answer_html = crawl_answer_from_question(question_for_query)
            question_for_query.answer_html = answer_html.encode('utf-8')
            question_for_query.save()
        answer_html = question_for_query.answer_html
        return answer_html


def crawl_answer_from_question(question):
    if question.stackoverflow_link:
        response = requests.get(question.stackoverflow_link)
        soup = BeautifulSoup.BeautifulSoup(response.content)
        answer_id = 'answer-' + str(question.accepted_answer_id)
        answer_div = soup.find('div', {'id': answer_id})
        answer_html = ''
        answer = answer_div.find('td', {'class': 'answercell'})
        if answer:
            answer_html = str(answer)
        return answer_html
