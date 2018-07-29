#!/bin/bash

nohup uwsgi --http 0.0.0.0:80 --master --module app:app --processes 4 > /opt/logs/uwsgi.log 2>&1 &
