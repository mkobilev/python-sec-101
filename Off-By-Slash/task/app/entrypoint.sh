#!/bin/bash
RUN_PORT="8080"
gunicorn app:app --bind "0.0.0.0:8080" --daemon
nginx -g 'daemon off;'