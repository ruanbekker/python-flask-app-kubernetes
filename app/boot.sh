#!/bin/sh
export DB_SEED=${DB_SEED:-False}
export DB_TYPE=${DB_TYPE:-sqlite}

if [ "${DB_TYPE}" = "mysql" ]
then 
  export DB_URI="mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST/$MYSQL_DATABASE"
fi

gunicorn server:app \
	--workers 1 \
	--threads 1 \
	--bind 0.0.0.0:8080 \
	--capture-output \
	--access-logfile '-' \
	--error-logfile '-'
