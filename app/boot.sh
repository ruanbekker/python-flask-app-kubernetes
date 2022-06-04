#!/bin/sh
gunicorn server:app \
	--workers 2 \
	--threads 2 \
	--bind 0.0.0.0:8080 \
	--capture-output \
	--access-logfile '-' \
	--error-logfile '-'
