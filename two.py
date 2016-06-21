import inspect
import logging
def test():
    who = logging.getLogger('two')
    print(who)
    who.critical('msg from two')
    print(inspect.stack()[0][3])
