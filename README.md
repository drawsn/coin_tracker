# Coin Tracker

** A cryptocurrency managing app written in Python3/Django.**

Author: Aron Hampersberger <a.hampersberger@gmail.com>

## Introduction

For owners of different crypto currencies it is a lot of effort to keep track of the current value of their holdings and how much they are worth in fiat currency.

This app provides the user the functions to add currency balances for different crypto currencies. These balances can be calculated in fiat currency by the help of implemented apis.

for more information and currently available use cases view "DESIGN_PAPER.txt"

## Getting the code

```
 $ git clone https://aronh@bitbucket.org/aronh/coin_tracker.git
 $ cd coin_tracker
```

## Building

I recommend to install dependencies in an own python virtualenv:
```
$ virtualenv myapp/
$ source myapp/bin/activate
```

Install dependencies with 'pip':
```
 - [Requests](http://docs.python-requests.org/en/latest/)
 - apt-get install libpq-dev
 - json
 - psycopg2
```
 
Install latest Django version:
```
$ git clone git://github.com/django/django.git django-trunk
$ pip3 install -e django-trunk/
```

Install postgresql database:
```
$ deactivate
$ sudo apt-get install libpq-dev python-dev
$ sudo apt-get install postgresql postgresql-contrib
```

Setup postgresql DB:
```
$ sudo su - postgres
$ createdb coin_tracker
$ createuser -P
$ psql
$ GRANT ALL PRIVILEGES ON DATABASE coin_tracker TO myuser;
```

Migrate DB:
from project root >
$ cd coin_tracker/settings.py
open settings.py and edit the DATABASES section to match your postgresql settings

from project root:
$ python3 manage.py migrate

Start the django server:
$ python3 manage.py runserver

Run tests:
$ python3 manage.py test


Admin interface: http://yourserver:port/admin/
User interface: http://yourserver:port/balance_manager/


## License
GPL v3 see LICENSE.txt