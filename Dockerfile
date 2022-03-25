FROM python:3.7-buster
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "$PATH:/root/.local/bin/"

RUN mkdir /src
WORKDIR /src

COPY poetry.lock  poetry.toml pyproject.toml ./
RUN poetry install

COPY . .

EXPOSE 5000

ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "-b", "0.0.0.0:5000"]
