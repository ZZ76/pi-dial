import RPi.GPIO as GPIO
from queue import Queue
import time
import argparse

'''
connection
  Dial |  Pi
   4   |  GND
   5   |  GPIO
--------------
GPIO PUD_UP
'''

in_port = 16
max_size = 120
pulse_freeze = 30
q = list()
signal = list()
Q_high = list()
Q_low = list()
numbers = list()

GPIO.setmode(GPIO.BCM)
GPIO.setup(in_port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def signal_to_pulse():
    '''replace 0 with _, 1 with - '''
    global signal
    pulses = ['_' if s == 0 else '-' for s in signal]
    return ''.join(pulses)

def process_sig(signal):
    '''
    p_tmp: sum of continued high(1) pulse
    zero_cnt: count of continued low(0) pulse
    '''
    global Q_high, Q_low
    p_tmp = 0
    zero_cnt = 0
    for s in signal:
        p_tmp += s
        if s == 0:
            zero_cnt += 1
            if p_tmp >0:    # if signal change from 1 to 0, then add p_tmp to Q_high and reset p_tmp
                Q_high.append(p_tmp)
                p_tmp = 0
        if s == 1 and zero_cnt > 0:     # if signal change from 0 to 1
            Q_low.append(zero_cnt)
            zero_cnt = 0
    #print(f'{Q_high} {len(Q_high)} {signal}', end='')
    #print(f'\nHigh:{Q_high}\nLow:{Q_low}', end='')
    if any(x < 6 or x > 10 for x in Q_high) or any(x > 3 or x < 2 for x in Q_low[1:]):  # invalid situation
        ''' check number of continued high and low pulse '''
        Q_high = list()
        Q_low = list()
        return
    if len(Q_high) > 0:
        #print(f'\r{len(Q)}')
        #print(f'\nHigh:{Q_high}\nLow:{Q_low}', end='')
        numbers.append(str(10 - len(Q_high)))
        num = ''.join(numbers)
        print(f'\r{" "*max_size}', end='')
        print(f'\r{signal_to_pulse()}\nNumber: {10 - len(Q_high)}\n{num}')
        #print(f'\r{num}', end='')
    Q_high = list()
    Q_low = list()


def append_sig(p):
    # no input for 10 pulses, refresh
    global signal
    if signal[-10:] == [0] * 10:
        if sum(signal) > 5:
            process_sig(signal)
        signal = list()
    else:
        signal.append(p)

def append(q, p):
    global signal, pulse_freeze
    if len(q) >= max_size:
        q_tmp = q[1:]
    else:
        q_tmp = q
    q_tmp.append(p)
    append_sig(1 if p=='-' else 0)
    if len(q) >= max_size and pulse_freeze:
        if q_tmp[-pulse_freeze:] == ['_'] * pulse_freeze:
            return q
    return q_tmp

def main():
    global q
    try:
        while True:
            if GPIO.input(in_port):
                q = append(q, '-')
            else:
                q = append(q, '_')
            output = ''.join(q)
            print(f'\r{output}', end='')
            time.sleep(0.01)
    except BaseException as e:
        print('\r')
        print(e)
        GPIO.cleanup()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--freeze', action='store_true')
    args = parser.parse_args()
    if args.freeze:
        pass
    else:
        pulse_freeze = 0
    main()
