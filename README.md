# pi_dial
read NZ rotary dial's input from a retro phone using raspberry pi
<br /><br />
reverse arranged dial in NZ
<br />
<img src="https://github.com/ZZ76/pi_dial/blob/main/images/face.jpg" width="250">
<br />

### Wiring:
| Dial |  Pi |
|:---:|:---:|
|4|  GND |
|5|  GPIO16 |
|3|  GPIO20 |
<div>
<img src="https://github.com/ZZ76/pi_dial/blob/main/images/back.jpg" width="250">
<img src="https://github.com/ZZ76/pi_dial/blob/main/images/wired.jpg" width="250">
</div>

### Example of signal:
                  |    while dialing, p5 will toggle until the dial back to its home position    |

    p5: __________--------------------------------------------------------------------------------_______________
    p3: _________________________________________--------___-------___--------___-------___-------_______________

                             |      when released, the rotary dial will start rotating back      |
                             |            and sending pulses to p3 on its way back               |
                                                 |      this piece in p3 is the signal to be     |
                                                 |       processed and read the number from      |
    input_number = 10 - pulse_count
### Usage:
use argument `-f` to freeze the signal
|file||
|:---:|---|
| v1.py | only 2 wires connect to port 4 and 5, can just read the number but not robust |
| v2.py | 3 wires version, the proper way of connection |
| read_gpio.py | visualise gpio input, read from GND by default for debugging. use `-p` `port_number` to select port, use `-l` set port to PUD_DOWN which is PUD_UP by default |

### Signals for all the number:
reading interval is set to 0.01s

    -------___--------__--------___--------__--------___-------___--------___-------___--------___------                    
    Number: 0

    --------__--------__--------___--------___-------___--------__--------___-------___-------                              
    Number: 1

    --------___--------__--------___-------___--------___-------___--------__-------                                        
    Number: 2

    --------__--------___-------___--------___-------___--------___------                                                   
    Number: 3

    --------___--------___-------___--------__--------___-------                                                            
    Number: 4

    --------___-------___--------___-------___-------                                                                       
    Number: 5

    --------___-------___--------__-------                                                                                  
    Number: 6

    --------__--------___-------                                                                                            
    Number: 7

    --------__-------                                                                                                       
    Number: 8

    -------                                                                                                                 
    Number: 9
