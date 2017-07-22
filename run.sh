#!/bin/bash -x

gunicorn -b 127.0.0.1:5000 --backlog 100 --workers 4 wsgi:app --log-level info --acess-logfile $VSLBOT_ACCESS_LOG --error-logfile $VSLBOT_ERROR_LOG
