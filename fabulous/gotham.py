"""
    fabulous.gotham
    ~~~~~~~~~~~~~~~

    This is a gimmick feature that generates silly gothic poetry.

    This uses a simple mad lib algorithm. It has no concept of meter or rhyme.
    If you want a *proper* poetry generator, check out poemy2_ which uses markov
    chains and isledict. It's written by the same author as Fabulous.

    This module can be run as a command line tool::

        jart@compy:~$ fabulous-gotham
        jart@compy:~$ python -m fabulous.gotham

    .. _poemy2: https://github.com/jart/poemy2

"""

import sys
import random
import itertools


them = ['angels', 'mourners', 'shadows', 'storm clouds', 'memories', 'condemned',
        'hand of Heaven', 'stroke of death', 'damned', 'witches', 'corpses']
them_verb = ['follow', 'hover close', 'approach', 'loom', 'taunt',
             'laugh', 'surround', 'compell', 'scour']
adj = ['cold', 'dead', 'dark', 'frozen', 'angry', 'ghastly', 'unholy', 'cunning', 'deep',
       'morose', 'maligned', 'rotting', 'sickly']
me_part = ['neck', 'heart', 'head', 'eyes', 'soul', 'blood', 'essence', 'wisdom']
feeling = ['pain', 'horror', 'frenzy', 'agony', 'numbness', 'fear', 'love',
           'terror', 'madness', 'torment', 'bitterness', 'misery']
angst = ['care', 'understand', 'question']
me_verb = ['flee', 'dance', 'flail madly', 'fall limply', 'hang my head', 'try to run',
           'cry out', 'call your name', 'beg forgiveness', 'bleed', 'tremble', 'hear']
action = ['sever', 'crush', 'mutilate', 'slay', 'wound', 'smite', 'drip',
          'melt', 'cast', 'mourn', 'avenge']
place = ['the witching hour', 'the gates of hell', 'the door', 'the path', 'death',
         'my doom', 'oblivion', 'the end of life', 'Hell', 'nothingness', 'purgatory',
         'void', 'earth', 'tomb', 'broken ground', 'barren land', 'swirling dust']


def lorem_gotham():
    """Cheesy Gothic Poetry Generator

    Uses Python generators to yield eternal angst.

    When you need to generate random verbiage to test your code or
    typographic design, let's face it... Lorem Ipsum and "the quick
    brown fox" are old and boring!

    What you need is something with *flavor*, the kind of thing a
    depressed teenager with a lot of black makeup would write.
    """
    w = lambda l: l[random.randrange(len(l))]
    er = lambda w: w[:-1]+'ier' if w.endswith('y') else (w+'r' if w.endswith('e') else w+'er')
    s = lambda w: w+'s'
    punc = lambda c, *l: " ".join(l)+c
    sentence = lambda *l: lambda: " ".join(l)
    pick = lambda *l: (l[random.randrange(len(l))])()
    while True:
        yield pick(
            sentence('the',w(adj),w(them),'and the',w(them),w(them_verb)),
            sentence('delivering me to',w(place)),
            sentence('they',w(action),'my',w(me_part),'and',w(me_verb),'with all my',w(feeling)),
            sentence('in the',w(place),'my',w(feeling),'shall',w(me_verb)),
            sentence(punc(',', er(w(adj)),'than the a petty',w(feeling))),
            sentence(er(w(adj)),'than',w(them),'in',w(place)),
            sentence(punc('!','oh my',w(me_part)),punc('!','the',w(feeling))),
            sentence('no one',s(w(angst)),'why the',w(them),w(them_verb + me_verb)))


def lorem_gotham_title():
    """Names your poem
    """
    w = lambda l: l[random.randrange(len(l))]
    sentence = lambda *l: lambda: " ".join(l)
    pick = lambda *l: (l[random.randrange(len(l))])()
    return pick(
        sentence('why i',w(me_verb)),
        sentence(w(place)),
        sentence('a',w(adj),w(adj),w(place)),
        sentence('the',w(them)))


def main():
    """I provide a command-line interface for this module
    """
    print
    print "-~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~-"
    print lorem_gotham_title().center(50)
    print "-~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~--~*~-"
    print
    poem = lorem_gotham()
    for n in range(16):
        if n in (4, 8, 12):
            print
        print poem.next()
    print


if __name__ == '__main__':
    main()
