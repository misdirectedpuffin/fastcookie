FROM python:3.11.0

ENV PYTHONASYNCIODEBUG=1

ARG INSTALL_DEV=false
ARG POETRY_VERSION=1.3.1

ENV PYTHONPATH=/app

EXPOSE 80

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - \
  && cd /usr/local/bin \
  && ln -s /root/.local/bin/poetry

RUN apt update -y \
  && apt upgrade -y \
  && apt -y install \
  libolm-dev \
  unzip \
  curl \
  gcc \
  git \
  jq \
  uuid-runtime \
  && poetry config virtualenvs.create false

WORKDIR /app/

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml poetry.lock* /app/

# Allow installing dev dependencies to run tests
RUN bash -c "if [ $INSTALL_DEV == 1 ] ; then poetry install --no-root --with dev ; else poetry install --no-root ; fi"

COPY ./gunicorn/start.sh /start.sh
COPY ./gunicorn/gunicorn_conf.py /gunicorn_conf.py
RUN chmod +x /start.sh

COPY . .
# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
