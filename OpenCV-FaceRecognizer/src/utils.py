#Copyright (c) 2013-2018 Hanson Robotics, Ltd.
def split(seq, gen):
    """ Split 'seq' at every element that 'gen' yields True to. """
    gen.next() # Get to the first yield in the generator
    j = 0
    for i, el in enumerate(seq):
        if gen.send(el):
            yield seq[j:i]
            j = i
    yield seq[j:]


def capacitor(limit, key=lambda x: x):
    """
    Accumulate the value sent through 'yield' statements and yield True every
    time the accumulator (i.e. charge) reaches the limit.
    """
    charge = 0
    el = yield True
    while True:
        charge += key(el)
        if charge > limit:
            # "Discharge" the capacitor and add the overflowing element to it.
            charge = key(el)
            # Signal an overflow
            el = yield True
        else:
            # Signal an eventless charge
            el = yield False

def getcenter(box):
    x, y, w, h = box
    return (x + w/2, y + h/2)
