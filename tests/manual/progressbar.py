#!/usr/bin/env python

from terminate.widget import ProgressBar
import time

p = ProgressBar('bar')
p.update(0)
time.sleep(.2)
p.update(20, 'safe epam and eggs')
time.sleep(.2)
p.update(50, None)
time.sleep(.2)
p.update(40)
time.sleep(.2)
p.set_title('baz')
p.update(20, 'spam and eggs')
time.sleep(.2)
p.update(70)
time.sleep(.2)
p.update(80)
time.sleep(.2)
p.update(100)
