#!/usr/bin/env python
#
# Copyright 2016 The Fabulous Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""I am *not* responsible if this causes severe physical or mental injury
"""

from terminate.term import display, stdout, Magic
        

try:
    while True:
        for c in Magic.COLORS.iterkeys():
            stdout.write(display(bg=c))
            stdout.move('down',4)
except KeyboardInterrupt:
    stdout.write(display('default'))
    print
    print "Interupt from keyboard. Exiting."
