# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change).

To run the app, you will need a Trello board, api key and api token. First [create a Trello account](https://trello.com/signup) and then generate an api key and token following the instructions [here](https://trello.com/app-key). Add these to the `.env` file. Using the [Trello website](https://trello.com/), create a new board and add the board id (which should be in the url when looking at the board on Trello) to the `.env` file.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Tests

The unit and integration tests are written using pytest and are kept in the `tests` folder. You can run them all with the command
```bash
$ poetry run pytest tests
```

The unit tests are kept in the `unit_tests` subfolder. You can run only unit tests using the command
```bash
$ poetry run pytest tests/unit_tests
```

The integration tests are kept in the `integration_tests` subfolder.
They use the env.test environment.
You can run only integration tests using the command
```bash
$ poetry run pytest tests/integration_tests
```

## End to End Tests

The end to end tests are in a separate folder called `tests_e2e`.

To run the end to end tests, you will need to download the [Firefox browser](https://www.mozilla.org/en-GB/firefox/windows/) and the [geckodriver](https://github.com/mozilla/geckodriver/releases) executable. Add the geckodriver executable's location to your path environment variable.

To run these tests, you need to be able to create a board on trello automatically, for which you need your organization id from trello. The end to end tests use your `.env` file, so add it there.

You can get your organization id from making a request to trello, such as a `GET /boards/` request, or from watching requests made by your browser when on the trello website using developer tools.

They run in headless mode by default - if you need to be able to see the Firefox window they are controlling, set
```
opts.headless = False
```
in the driver fixture of `test_todo_app.py`. When running in docker (see below), headless mode must be used.

You can run the end to end tests using the command
```bash
$ poetry run pytest tests_e2e
```

## Ansible

This app can be managed across virtual machines using ansible. For more instructions, see the README in the ansible folder.

## Docker

This app is set up to run in docker, either in production mode or development mode.

### Production

You can build and run the app with docker in production mode.

```bash
$ docker build --target production --tag todo-app:prod .
$ docker run -p 8080:5000 --env-file .env todo-app:prod
```

### Development

You can build and run the app with docker compose in development mode. This is an alternative to the instructions to run locally. You will need [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed for this.

You will still need to copy .env.template and set up the .env file (see above for instructions), but all other dependencies will be handled automatically. 

```
$ docker compose up
```

The app should then be available at localhost:8080. To stop the service you can use the command line or the Docker Desktop interface.

The app should automatically update when you make changes to the code. However, when new dependencies are added to the pyproject.toml you will need to rebuild the image, using
```
$ docker-compose up --build
```

### Test

You can run all the tests using docker.
This is used by Github Actions to run the tests against each push and each pull request.

The tests should not use your live boards but you can create a new .env file without a dummy board id and use that instead. The end-to-end tests do require a trello api key and token, and your organization id.

```bash
$ docker build --target test --tag todo-app:test .
$ docker run --env-file .env todo-app:test
```

## Heroku

Github actions deploys to Heroku whenever you push to the main branch.

The todo app can be viewed at: [https://kirsty-land-todo-app.herokuapp.com/](https://kirsty-land-todo-app.herokuapp.com/)
