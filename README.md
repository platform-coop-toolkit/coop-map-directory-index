# Platform Co-op Directory

## Prerequisites

This project requires:

- [Python 3.x](https://www.python.org/downloads/) (it's been running under 3.6 & 3.7)
- [PostgreSQL](https://www.postgresql.org/download/) with [PostGIS extensions](https://postgis.net/install/)
- [Node 12.x](https://nodejs.org/en/download/) and NPM
- A [Mapbox](https://mapbox.com/) developer key
- A [Here](https://developer.here.com/) developer key

## Installation

1. `git clone` this repository and change into the resulting directory.
2. Create a virtual environment: `python3 -m venv .cmdi`
3. Activate the virtual environment: `source .cmdi/bin/activate`
4. Install the Python requirements: `pip install -r requirements.txt`
5. Create a PostgreSQL role for this project: `createuser --password cmdi`
6. Create the PostgreSQL database: `createdb --owner cmdi cmdi`
7. Import the current database: `bunzip2 < scratch/cmdi.sql.bz2 | psql --set ON_ERROR_STOP=on -h localhost cmdi`
8. Copy `.env-example` to `.env` and fill in the appropriate credentials.
9. Copy `Procfile-example` to `Procfile` and make sure the appropriate section for your environment is uncommented.
10. Install and build assets: `npm install && npm run build`
11. For a local installation, start the server: `honcho start`

### Docker Installation

TODO.

## Contributing

- Be consistent in using American English for interface elements.
- Be consistent in using sentence case for interface elements and headers.

Ultimately the Directory will be presented in multiple, translated languages.

## Data

__19 March 2020__: Flipped the switch on account creation in production and so the flow of definitive data has reversed, now it's from production to development.

Remote:

```bash
pg_dump -U cmdi -h localhost -f scratch/cmdi.sql --clean --if-exists --no-privileges --no-acl --no-owner cmdi && bzip2 -9 --force scratch/cmdi.sql
```

Local:

```bash
scp ubuntu@demo.directory.platform.coop:/home/ubuntu/coop-map-directory-index/scratch/cmdi.sql.bz2 scratch/
bunzip2 < scratch/cmdi.sql.bz2 | psql --set ON_ERROR_STOP=on -h localhost cmdi
```

__January 2020__: Data is being managed outside of this repository. A locally-installed development database is periodically dumped, transferred, and imported into the production server.

Local:

```bash
pg_dump -U cmdi -h localhost -f scratch/cmdi.sql --clean --if-exists cmdi && bzip2 -9 --force scratch/cmdi.sql
scp scratch/cmdi.sql.bz2 ubuntu@awshost:/home/ubuntu/coop-map-directory-index/scratch
```

Remote:

```bash
bunzip2 scratch/cmdi.sql.bz2
sudo su postgres
psql --set ON_ERROR_STOP=on -h localhost -U cmdi -W -f scratch/cmdi.sql cmdi
exit
honcho start
```

## Development

Limit commit messages to 72 characters, do not end with a full stop, prefix with one of:

- `build`
- `ci`
- `chore`
- `docs`
- `feat`
- `fix`
- `perf`
- `refactor`
- `revert`
- `style`
- `test`

For more information, [see here](https://www.conventionalcommits.org/en/v1.0.0/#summary).

Use `dev` branch as the basis for all pull requests/feature development.

Use the `master` branch for "stable" code (merge from `dev` periodically).

## Notes

Modules we may need further down the road:

- [django-languages-plus](https://github.com/cordery/django-languages-plus)
- [django-countries-plus](https://github.com/cordery/django-countries-plus)
- [pycountry](https://pypi.org/project/pycountry/)
- [py-moneyed](https://github.com/limist/py-moneyed)
