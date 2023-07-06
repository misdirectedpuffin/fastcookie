#! /bin/bash
set -e

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}


# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"

if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-80}"
LOG_LEVEL="${LOG_LEVEL:-debug}"
DEBUGGER="${DEBUGGER:-false}"

if [[ "$ENV" = development && "${DEBUGGER}" = true ]]; then
    exec sh -c "python -m debugpy --wait-for-client --listen 0.0.0.0:5678 /usr/local/bin/uvicorn main:app --reload --host $HOST --port 80"
# Run with no debugger in dev mode.
elif [[ "$ENV" = development && "${DEBUGGER}" = false ]]; then
    exec /usr/local/bin/uvicorn --reload --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL" "$APP_MODULE"
# Run production mode.
else
    if [ -f /app/gunicorn_conf.py ]; then
        DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
    elif [ -f /app/app/gunicorn_conf.py ]; then
        DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
    else
        DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
    fi
    export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
    export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
    # Start Gunicorn
    exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
fi
