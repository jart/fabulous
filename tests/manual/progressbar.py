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
