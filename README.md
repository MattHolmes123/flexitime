# flexitime

Flexitime is a work in progress application to record users shifts and calculates their overtime. 

It has been written using Python 3.6 and Django.


## First-time setup

1. Clone project from GitHub, cd to its directory.

2. Run `./setup-local.sh` to do the following things:
    1. Create a virtual environment using virtualenv and install all requirements.
    2. Run all migrations.
    3. Create a test admin user, with some test data populated.

## Running

1. Run `python manage.py runserver`

2. Connect to `http://127.0.0.1:8000/` in your browser. 

## Testing

1. To run all tests: `./run-tests.sh`
2. To run all tests with coverage: `./run-tests-coverage.sh`
