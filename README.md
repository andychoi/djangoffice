
# Django Simple Office, Timesheet

https://django.readthedocs.io/en/1.4.X/topics/generic-views-migration.html


Create a virtual environment and activate it with *(Optional)*::

virtualenv --python=python2.7  venv 
source venv/bin/activate

    $ python -m venv .venv && source .venv/bin/activate

Install dependencies with::

    $ python -m pip install --upgrade pip wheel
    $ python -m pip install -r requirements.txt

Determine database to use, sqllite or postgresql
    $ vi psmprj/settings.py

Create the database with::

    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createcachetable     # create cache table when using Postgres


## test 
$ python manage.py djo_demo

```
user id, password = demo
testuser
testpm
testmanager
```

## renderer error

https://stackoverflow.com/questions/54339582/fix-render-got-an-unexpected-keyword-argument-renderer-in-django-2-1


## get serial number

https://stackoverflow.com/questions/67084479/django-model-generate-series-number-for-each-identifier-upon-saving-the-model
https://stackoverflow.com/questions/14234917/django-how-to-get-self-id-when-saving-a-new-object