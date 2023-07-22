import RPi.GPIO as GPIO
from queue import Queue
import time
import argparse

port = 20
max_size = 120
pull = GPIO.PUD_UP
q = list()

def append(q, e):
    global max_size
    if len(q) >= max_size:
        q = q[1:]
    q.append(e)
    return q

def main():
    global port, q, pull
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.IN, pull_up_down=pull)
    while True:
        if not GPIO.input(port):
            q = append(q, '-')
        else:
            q = append(q, '_')
        output = ''.join(q)
        print(f'\r{output}', end='')
        time.sleep(0.01)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--low', action='store_true')
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    if args.low:
        pull = GPIO.PUD_DOWN
    if args.port:
        port = args.port
        print(f'using port {port}')
    try:
        main()
    except BaseException as be:
        print('\r')
        print(be)
        GPIO.cleanup()

