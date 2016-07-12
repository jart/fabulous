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

import logging
import itertools

from fabulous.logs import *
from fabulous.gotham import *
from fabulous.color import *

try:
  next
except NameError:
  next = lambda x: x.next()


logger = logging.getLogger('fabulous')


def luv():
    msg = "hello there how are you?  i love you!  sincerely compy <3 <3"
    while True:
        for n in itertools.chain(range(len(msg)), reversed(range(len(msg)))):
            yield msg[:n+1]


def bad_things():
    yield red("godzilla attack")
    yield bold(red("magnetic poles reverse"))
    yield red("caffeine use criminalized")
    yield bold(red("more horrible things happening...."))
    yield highlight_red("THIS INFORMATION IS NOT BEING DROWNED OUT!")
    yield bold(red("hip hip hooray"))


def test_transientlogger():
    import random, time
    happy, nightmare = luv(), bad_things()
    try:
        while True:
            if random.randrange(60) == 0:
                logger.warning(next(nightmare))
            else:
                logger.debug(next(happy))
            time.sleep(0.02)
    except StopIteration:
        pass


def test_transientlogger2():
    import time, random
    gothic = lorem_gotham()
    try:
        while True:
            if random.randrange(20) == 0:
                logger.warning(red(next(gothic)))
            else:
                logger.debug(next(gothic))
            time.sleep(0.1)
    except StopIteration:
        pass


if __name__ == '__main__':
    basicConfig(level=logging.WARNING)
    logging.warning("RUNNING TEST: test_transientlogger()")
    test_transientlogger()
    logging.warning("RUNNING TEST: test_transientlogger2()")
    test_transientlogger2()
