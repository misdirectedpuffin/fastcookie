FROM python:3.11.0

ARG POETRY_VERSION=1.5.1

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - \
    && cd /usr/local/bin \
    && ln -s /root/.local/bin/poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
RUN bash -c "if [ $INSTALL_DEV == 1 ] ; then poetry install --no-root --with dev ; else poetry install --no-root ; fi"

# WORKDIR /opt
RUN groupadd 1024
RUN chown :1024 /opt
RUN chmod 775 /opt
RUN chmod g+s /opt
RUN addgroup --gid 1024 appgrp
RUN adduser --disabled-password --gecos "" --force-badname --ingroup 1024 appuser
USER appuser

ADD . .
CMD [ "cookiecutter", "-f", "/app" ]
