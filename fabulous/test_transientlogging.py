
import logging

from fabulous.logs import *
from fabulous.gotham import *
from fabulous.color import *


logger = logging.getLogger('fabulous')


def luv():
    msg = "hello there how are you?  i love you!  sincerely compy <3 <3"
    while True:
        for n in range(len(msg)) + list(reversed(range(len(msg)))):
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
                logger.warning(nightmare.next())
            else:
                logger.debug(happy.next())
            time.sleep(0.02)
    except StopIteration:
        pass


def test_transientlogger2():
    import time, random
    gothic = lorem_gotham()
    try:
        while True:
            if random.randrange(20) == 0:
                logger.warning(red(gothic.next()))
            else:
                logger.debug(gothic.next())
            time.sleep(0.1)
    except StopIteration:
        pass


if __name__ == '__main__':
    basicConfig(level=logging.WARNING)
    logging.warning("RUNNING TEST: test_transientlogger()")
    test_transientlogger()
    logging.warning("RUNNING TEST: test_transientlogger2()")
    test_transientlogger2()
