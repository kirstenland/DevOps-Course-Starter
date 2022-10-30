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

To run the app, you will need an Azure where you should set up a CosmosDB cluster. Once you've set this up, you can get your connection string from "PRIMARY CONNECTION STRING" for your CosmosDB cluster, available under Settings → Connection String. Add this to the `.env` file.

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

### Authentication and Authorization

The todo app uses Github's OAuth to log in users.
All users can view todos, but only allow users with the "WRITER" role can add todos or complete todos.

In the tests, and in dev when not testing authorization, setting the environment variable `LOGIN_DISABLED=True` will disable authentication and the user will have role WRITER.

If you need to test the authentication flow, or are deploying to a prod or QA site, you will need to create an OAuth App, following the instructions [here](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps). Adding the client id and the client secret to the environment variables, and setting `LOGIN_DISABLED=False` will then enable authentication.

Add the ids of any user with the "WRITER" role to the config file.

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

To run these tests, you need your connection string to connect to your Cosmos cluster. The tests should use a different database from the one you use in dev, but can use the same Cosmos cluster.

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

The tests should not use your live boards but you can create a new .env file without a dummy board id and use that instead. The end-to-end tests do require your mongo connection string.

```bash
$ docker build --target test --tag todo-app:test .
$ docker run --env-file .env todo-app:test
```

## Azure

The app is deployed to Azure from the Docker Hub container registry, with resources set up via terraform.

The terraform state is stored in a shared blob storage account on Azure called `krldevopstodoapptfstate`.
You can manually apply terraform changes by obtaining an `ARM_ACCESS_KEY` for the blob storage and running `terraform init` followed by `terraform apply`.

Terraform changes should be applied automatically on Github Actions whenever a commit is pushed to the main branch.
Github actions also pushes to the Docker Hub container registry and restarts the Azure app through a webhook.

The todo app can be viewed at: [https://prod-terraformed-todoapp.azurewebsites.net/](https://prod-terraformed-todoapp.azurewebsites.net/)
