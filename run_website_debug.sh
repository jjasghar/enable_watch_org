#!/bin/bash

source venv/bin/activate
export FLASK_APP=app
export FLASK_DEBUG=true

export APP_SECRET_KEY=$(python -c 'import os; print (f"{os.urandom(24).hex()}")')

flask run