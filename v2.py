import RPi.GPIO as GPIO
from queue import Queue
import time
import argparse

'''
connection
Rotary |  Pi
   4   |  GND
   5   |  16
   3   |  20
--------------
GPIOs PUD_UP

interval 0.01s
high levels count 6 to 8
low levels count  2 to 3

example of signal:
              |   while dialing, p5 will toggle until the dial back to its home position   |

p5: __________--------------------------------------------------------------------------------_______________
p3: _________________________________________--------___-------___--------___-------___-------_______________

                         |      when released, the rotary dial will start rotating back      |
                         |            and sending pulses to p3 on its way back               |
                                             |      this piece in p3 is the signal to be     |
                                             |       processed and read the number from      |
'''

p5 = 16
p3 = 20
max_size = 120 # max length for displaying
pulse_freeze = 20 # stop displaying new inputs after receive continuous n singals
q = list() # queue for displaying all input signals
signal = list() # input signals for analysing
Q_high = list() # high level in $signal, [6, 7, 8] means 6, 7, 8 continuous high levels in $signal
Q_low = list() # low level in $signal, [2, 3, 3] means 2, 3, 3 continuous low levels in $signal
numbers = list() # all input numbers

GPIO.setmode(GPIO.BCM)
GPIO.setup(p5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(p3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def signal_to_pulse():
    '''replace 0 with _, 1 with - '''
    global signal
    pulses = ['_' if s == 0 else '-' for s in signal]
    return ''.join(pulses)

def process_sig():
    '''
    p_tmp: sum of continued high(1) pulse
    zero_cnt: count of continued low(0) pulse
    '''
    global Q_high, Q_low, signal
    p_tmp = 0
    zero_cnt = 0
    for i, s in enumerate(signal):
        p_tmp += s
        if s == 0:
            zero_cnt += 1
            if p_tmp >0:    # if signal change from 1 to 0, then add p_tmp to Q_high and reset p_tmp
                Q_high.append(p_tmp)
                p_tmp = 0
        if s == 1:
            if zero_cnt > 0:     # if signal change from 0 to 1
                Q_low.append(zero_cnt)
                zero_cnt = 0
        if i == len(signal) - 1:  # check if it is the last element
            if s == 1: # add p_tmp to Q_high
                Q_high.append(p_tmp)
    #print(f'\n{Q_high} {len(Q_high)} {signal}', end='')
    #print(f'\nHigh:{Q_high}\nLow:{Q_low}', end='')
    if any(x < 6 or x > 10 for x in Q_high) or any(x > 3 or x < 2 for x in Q_low[1:]):  # invalid situation, reset
        ''' check number of continued high and low pulse '''
        Q_high = list()
        Q_low = list()
        signal = list()
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

def append(q, s):
    global pulse_freeze
    if len(q) >= max_size: # if exceed max_size, remove the first signal and append to the last
        q_tmp = q[1:]
    else:
        q_tmp = q
    q_tmp.append(s)
    if len(q) >= max_size and pulse_freeze:
        if q_tmp[-pulse_freeze:] == ['_'] * pulse_freeze:
            return q
    return q_tmp

def main():
    global q, signal
    try:
        while True:
            if GPIO.input(p3):
                if signal: # process
                    process_sig()
                    signal = list()
            else: # record
                if GPIO.input(p5):
                    signal.append(1)
                else:
                    if len(signal) > 0:  # ignore leading low levels while recording
                        signal.append(0)
            # display
            if GPIO.input(p5):
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
