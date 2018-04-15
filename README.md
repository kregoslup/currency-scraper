## Currency scraper
---

Opis architektury: 
Postawiłem sobie za cel stworzenie minimalistycznej aplikacji z jak najmniejszą
liczba zależności. Z tej racji skorzystałem z SQLite jako bazy danych. Aplikacja składa się z dwóch prostych modeli, jeden reprezentuje waluty,
natomiast drugi kurs waluty względem innej waluty. 

Dane są pobierane za pomocą prostego scrapera z użyciem `requests` oraz parsowane za pomocą `BeautifulSoup` następnie zapisywane do bazy.
Scrapowanie danych odbywa się cyklicznie za pomoca crona, ogranicza to niestety aplikację tylko do systemów operacyjnych posiadających mechanizm cronów.

Dane wystawiane są na dwóch adresach gdzie można je podejrzeć - jeden adres do listy walut, drugi do listy kursów.

Stworzone zostały też proste testy sprawdzające podstawowe funkcje.

----

### Instalacja:

* Na początku należy utworzyć virtualenv
* Za pomocą Makefile uzupełnionego wczesniej o scieżkę do katalogu z binarnymi plikami pythona: `make install`
* Ręcznie: `pip install -r requirements.txt`, następnie należy dodać wpis do crontab: 
`*/5 * * * * $(PYTHONDIR)/python manage.py runcrons > logs/cronjob.log`

### Odpalanie

* Makefile: `make run`
* `(virtualenv) manage.py runserver 0.0.0.0:8000`

### Co bym rozwinął:

* Zrezygnowałbym z SQLite na rzecz PostreSQL (ponieważ: https://www.sqlite.org/whentouse.html `(...)each SQLite database is only used by one connection.`)
* Zrezygnowałbym z pisanego ręcznie scrapera na rzecz gotowych narzędzi: Scrapy (https://scrapy.org/)
* Dodałbym wsparcie Dockera, przynajmniej dla lokalnego procesu developmentu aby zautomatyzować instalację
* Ansible do automatyzacji wdrożeń na serwer / Docker do automatyzacji wdrożeń na serwer
* Filtrowanie w restowym api na podstawie walut
* Dodałbym obsługę kolejek zadań zamiast crona: RQ i rq scheduler (http://python-rq.org/ https://github.com/rq/django-rq), celery (http://www.celeryproject.org/)
* Dodał typy i obsługę type checkera (http://mypy-lang.org/)
* Django admin
