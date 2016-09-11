# qstack
qstack is demo app that uses stackoverlow rest api to get list of questions
related to the query.
The questions returned from the query are indexed in the local database. The
answer for the questiono are retrieved lazily. If the question matches the user
query the answer is shown from local database if present else crawled from stackoverflow
indexed in local.

## To run on local server
cd qstack
run ./manage.py runserver
open 127.0.0.1/search/ in browser

