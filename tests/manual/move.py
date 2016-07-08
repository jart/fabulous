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

"""Outputs something like:
spaand eggs
george
"""

from fabulous.term import stdout

stdout.write('spam')
stdout.move('left')
stdout.write('and')
stdout.move('right')
stdout.write('eggs')
stdout.move('left',3)
stdout.move('down')
stdout.write('george')
print # trailing newline
