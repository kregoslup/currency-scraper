# SET THIS! To directory containing python binaries (probably your virtualenv)
# PYTHONDIR := /

.PHONY: install test run

install:
    $(PYTHONDIR)/pip install -r requirements.txt
    */5 * * * * $(PYTHONDIR)/python manage.py runcrons > logs/cronjob.log

test:
    $(PYTHONDIR)/python manage.py test

run
    $(PYTHONDIR)/python manage.py runserver 0.0.0.0:8000
