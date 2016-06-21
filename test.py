import asyncio
import random
import copy
import queue
import time
import sys

try:
   a={}
   print(a[1])
except:
   print(sys.exc_info())
 
class test(object):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
    def identity (self):
        return self
		
objIn=test('arg-1','arg-2','arg-3','arg-n',key1=1,key2=2,key3=3,keyn='n')
objOut=objIn.identity()
print('args=',objOut.args,'kwargs=',objOut.kwargs)
objIn.args = (1,2)
print('args=',objOut.args,'kwargs=',objOut.kwargs)

#If you want just the arguments to be printed...
print(test('arg-1','arg-2','arg-3','arg-n',key1=1,key2=2,key3=3,keyn='n').identity().args)
print(test('arg-1','arg-2','arg-3','arg-n',key1=1,key2=2,key3=3,keyn='n').identity().kwargs)


class test1(object):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
    def identity (self):
        return self.args

print(test1([1,2,3]).identity())
