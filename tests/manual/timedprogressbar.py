#!/usr/bin/env python

from terminate.widget import TimedProgressBar
import time
import random

p = TimedProgressBar('bar')
n = 100
for i in range(n):
    p.update(float(i)/n *100, 'update '+str(i))
    time.sleep(random.random())