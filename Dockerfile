FROM python:3.7-buster as base
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "$PATH:/root/.local/bin/"

RUN mkdir /app
WORKDIR /app

COPY poetry.lock  poetry.toml pyproject.toml ./
RUN poetry install


FROM base as production
COPY ./todo_app /app/todo_app
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "-b", "0.0.0.0:5000"]


FROM base as development
VOLUME [ "/app/todo_app" ] 
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]


FROM base as test
ENV GECKODRIVER_VER v0.30.0
 
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
