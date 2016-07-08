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

from __future__ import print_function

import sys


def printy(s):
    """Python 2/3 compatible print-like function"""
    if hasattr(s, 'as_utf8'):
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(s.as_utf8)
            sys.stdout.buffer.write(b"\n")
        else:
            sys.stdout.write(s.as_utf8)
            sys.stdout.write(b"\n")
    else:
        print(s)
