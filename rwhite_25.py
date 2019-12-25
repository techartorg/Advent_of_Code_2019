from rwhite_intcode import Ascii

bot = Ascii([int(i) for i in open('day_25.input').read().split(',')])

def wrap(func):
    def _w(*args, **kwargs):
        if not args:
            return bot.send_ascii(f'{func.__name__}')
        return bot.send_ascii(f'{func.__name__} {" ".join(str(a) for a in args)}')
    return _w

@wrap
def north(): pass

@wrap
def south(): pass

@wrap
def east(): pass

@wrap
def west(): pass

@wrap
def take(s): pass

@wrap
def drop(s): pass

@wrap
def inv(): pass
