FROM python:3.11-buster as base
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "$PATH:/root/.local/bin/"

RUN mkdir /app
WORKDIR /app

COPY poetry.lock  poetry.toml pyproject.toml ./


FROM base as production
RUN poetry install --without dev
COPY ./todo_app /app/todo_app
EXPOSE 5000
CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:${PORT:-5000}

FROM base as development
RUN poetry install
VOLUME [ "/app/todo_app" ]
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]


FROM base as test
RUN poetry install
ENV GECKODRIVER_VER v0.30.0
ENV SECRET_KEY "secret_key_for_ui_tests"

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr curl

# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

COPY ./todo_app /app/todo_app
COPY ./tests /app/tests
COPY ./tests_e2e /app/tests_e2e
COPY .env.test /app/.env.test
ENTRYPOINT ["poetry", "run", "pytest"]
