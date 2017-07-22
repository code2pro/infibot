#!/bin/bash -x

LOG_SUFFIX=$(date +%Y%m%d_%H%M%S)
VSLBOT_ACCESS_LOG=${VSLBOT_ACCESS_LOG}.${LOG_SUFFIX}
VSLBOT_ERROR_LOG=${VSLBOT_ERROR_LOG}.${LOG_SUFFIX}

gunicorn -b 127.0.0.1:5000 --backlog 100 --workers 4 \
    --log-level info --access-logfile $VSLBOT_ACCESS_LOG \
    --error-logfile $VSLBOT_ERROR_LOG \
    wsgi:app
