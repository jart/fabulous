
import random


def lorem_gotham():
    them = ['angels', 'mourners', 'shadows', 'storm clouds', 'memories', 'condemned'
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
    w = lambda l: l[random.randrange(len(l))]
    er = lambda w: w[:-1]+'ier' if w.endswith('y') else (w+'r' if w.endswith('e') else w+'er')
    s = lambda w: w+'s'
    punc = lambda c, *l: " ".join(l)+c
    sentence = lambda *l: lambda: " ".join(l)
    pick = lambda *l: (l[random.randrange(len(l))])()
    while True:
        yield pick(
            sentence('the',w(adj),w(them),'and the',w(them),w(them_verb),'and deliver me to',w(place)),
            sentence('they',w(action),'my',w(me_part),'and',w(me_verb),'with all my',w(feeling)),
            sentence('in the',w(place),'my',w(feeling),'shall',w(me_verb)),
            sentence(punc(',', er(w(adj)),'than the usual',w(feeling)), er(w(adj)),'than',w(them),'in',w(place)),
            sentence(punc('!','oh my',w(me_part)),punc('!','the',w(feeling))),
            sentence('no one',s(w(angst)),'why the',w(them),w(them_verb + me_verb)))
