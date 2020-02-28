## Coop Map Directory Index

### Prerequisites

This project requires Python 3 (it's been running under 3.6 & 3.7), PostgreSQL with PostGIS extensions, and a Mapbox developer key.

### Installation

1. `git clone` this repository.
2. Create a virtual environment: `python3 -m venv .cmdi`
3. Activiate the virtual environment: `source .cmdi/bin/activate`
4. Install the Python requirments: `pip install -r requirements.txt`
5. Create a PostgreSQL role for this project: `createuser --password cmdi`
6. Create the PostgreSQL database: `createdb --owner cmdi cmdi`
7. Import the current database: `bunzip2 -c ./scratch/cmdi.sql.bz2 | psql cmdi`
8. Copy `.env-example` to `.env` and fill in the appropriate credentials.
9. For a local installation simply start the server: `python manage.py runserver`


### Data

Data is presently being managed outside of this repository. A locally-installed development database is periodically dumped, transferred, and imported into the production server.

Local:
```
pg_dump -f scratch/cmdi.sql --clean --if-exists cmdi && bzip2 -9 --force scratch/cmdi.sql
scp scratch/cmdi.sql.bz2 ubuntu@awshost:/home/ubuntu/coop-map-directory-index/scratch
```

Remote:
```
sudo su postgres
bunzip2 scratch/cmdi.sql.bz2
psql -f scratch/cmdi.sql cmdi
exit
```

### Development

Limit commit messages to 72 characters, do not end with a full stop, prefix with one of:

* build
* ci
* chore
* docs
* feat
* fix
* perf
* refactor
* revert
* style
* test


### Notes

Modules we may need further down the road:
* [django-languages-plus](https://github.com/cordery/django-languages-plus)
* [django-countries-plus](https://github.com/cordery/django-countries-plus)
* [pycountry](https://pypi.org/project/pycountry/)
* [py-moneyed](https://github.com/limist/py-moneyed)
