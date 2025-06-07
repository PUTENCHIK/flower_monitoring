import socket
import time
import sys

host = 'db'
port = 3306
timeout = 10

start_time = time.time()
while True:
    try:
        with socket.create_connection((host, port), timeout=5):
            print("Database is available")
            sys.exit(0)
    except OSError:
        print("Waiting for database connection...")
        time.sleep(2)
    if time.time() - start_time > timeout:
        print("Timeout waiting for database")
        sys.exit(1)

