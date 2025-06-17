#!/bin/sh

python wait_for_db.py
python bot.py &
python main.py


