#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery -A app.tasks.celery_app:celery_app worker --loglevel=INFO
elif [[ "${1}" == "flower" ]]; then
    celery -A app.tasks.celery_app:celery_app flower
fi