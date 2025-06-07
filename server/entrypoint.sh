#!/bin/sh

python wait_for_db.py
alembic upgrade head
python bot.py &
python main.py


