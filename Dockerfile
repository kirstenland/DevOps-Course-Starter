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
