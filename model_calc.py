import importlib
import copy
import queue
import threading
import time

q=queue.Queue() #1

class ModelTarget(object):
    def __init__(self,*args,**kwargs):
        self._object = None
        self._module = None
        self._method = None

    def target(self,*args,**kwargs):
        if (kwargs.get('type') != 'generator'):
            self._object = q.get()
        else:
            self._module = importlib.import_module(kwargs.get('module'))  
            self._object = getattr(self._module,kwargs.get('class'))(*args,**kwargs)

        self._method=getattr(object,kwargs.get('method'))(*args,**kwargs) 

        if (kwargs.get('type') == 'generator'):
            q.put(copy.deepcopy(object)) 

        q.put(copy.deepcopy(object))
        return


#Model Input
def input(*args,**kwargs):
    model_calc=importlib.import_module('calculator')  #2
    calculator_object=getattr(model_calc,'calculator')(*args,**kwargs) #5
    input=getattr(calculator_object,'input')(*args,**kwargs) #7
    q.put(copy.deepcopy(calculator_object)) #10
    q.put(copy.deepcopy(calculator_object)) #10

## Model Add

def add(*args,**kwargs):
    calculator_object = q.get() #11
    add=getattr(calculator_object,'add')(*args,**kwargs) #7
    q.put(copy.deepcopy(calculator_object)) #


## Model Sub
def sub(*args,**kwargs):
    calculator_object = q.get()
    sub=getattr(calculator_object,'subtract')(*args,**kwargs)
    q.put(copy.deepcopy(calculator_object))

## Model print
def result(*args,**kwargs):
    calculator_object = q.get()
    res=getattr(calculator_object,'result')(*args,**kwargs)
    calculator_object = q.get()
    res=getattr(calculator_object,'result')(*args,**kwargs)

t1=threading.Thread(target=input,args=(q,))
t2=threading.Thread(target=add,args=(q,),kwargs={'extra':2})
t3=threading.Thread(target=sub,args=(q,))
t4=threading.Thread(target=result,args=(q,))
t1.start()
t1.join()
t2.start()
t3.start()
t2.join()
t3.join()
t4.start()

for i in range(2):
    keys=['module','class','method','type']
    values=['calculator','calculator','input','generator']
    kwargs=dict(zip(keys,values))
    t=threading.Thread(target=model,args=(q,),kwargs=kwargs)
    t.start()

for i in range(2):
    keys=['module','class','method','type','extra']
    values=['calculator','calculator','add','transfer',2]
    kwargs=dict(zip(keys,values))
    t=threading.Thread(target=model,args=(q,),kwargs=kwargs)
    t.start()

for i in range(2):
    keys=['module','class','method','type']
    values=['calculator','calculator','subtract','transfer']
    kwargs=dict(zip(keys,values))
    t=threading.Thread(target=model,args=(q,),kwargs=kwargs)
    t.start()

for i in range(4):
    keys=['module','class','method','type']
    values=['calculator','calculator','result','sink']
    kwargs=dict(zip(keys,values))
    t=threading.Thread(target=model,args=(q,),kwargs=kwargs)
    t.start()
