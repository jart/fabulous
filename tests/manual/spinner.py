#!/usr/bin/env python

from terminate.widget import Spinner
import time

s = Spinner()
for i in range(100):
    s.spin()
    time.sleep(.01)
