#!/usr/bin/env python

"""This is a long timed progress bar. Don't expect it to finish any 
time soon. It updates every 0 to 10 seconds. Send it a keyboard 
interupt (Ctrl-C) to stop."""

from terminate.widget import TimedProgressBar
import time
import random

print __doc__

p = TimedProgressBar('bar')
p.precision=10000
n = 100000
for i in range(n):
    p.update(float(i)/n *100, 'update '+str(i))
    time.sleep(random.random()* 10)