import one
import random
from ModelManager import ModelManager
def print_cache():
    three=one.One()
    result=[]
    for i in range(1000):
        result.append(three.get_a(random.randint(0,1000)))
    print(len(result))
    print(three.get_a.cache_info())

def print_nocache():
    three=one.One_nocache()
    print(three.get_a())

manager=ModelManager()
print(manager.getModelRefs())
