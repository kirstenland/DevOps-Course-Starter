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

You can run the end to end tests using the command
```bash
$ poetry run pytest tests_e2e
```

## Ansible

This app can be managed across virtual machines using ansible. For more instructions, see the README in the ansible folder.

## Docker

You can build and run the app with docker:

```
docker build --tag todo-app .
docker run -p 8080:5000 --env-file .env todo-app
```
