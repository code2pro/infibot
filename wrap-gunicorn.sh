#!/bin/bash -x

if [ -z ${LOG_SUFFIX} ]; then
    LOG_SUFFIX=$(date +%Y%m%d_%H%M%S)
fi
INFIBOT_ACCESS_LOG=${INFIBOT_ACCESS_LOG}.${LOG_SUFFIX}
INFIBOT_ERROR_LOG=${INFIBOT_ERROR_LOG}.${LOG_SUFFIX}

env

gunicorn -b 127.0.0.1:5000 --backlog 100 --workers 2 \
    --log-level info --access-logfile $INFIBOT_ACCESS_LOG \
    --error-logfile $INFIBOT_ERROR_LOG \
    wsgi:app
