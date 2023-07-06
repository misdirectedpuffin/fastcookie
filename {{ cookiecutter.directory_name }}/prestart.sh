#! /usr/bin/env bash

echo 'Waiting for backend db...'
python /app/scripts/backend_pre_start.py

if [ "${ENV}" == 'development' ]; then
    echo 'Run migrations...'
    alembic upgrade head
    echo 'Migration complete...'

    echo 'Run backend_post_start.py'
    # python /app/scripts/backend_post_start.py

else
    echo 'Skipping migrations...'
fi

python /app/scripts/initial_data.py

