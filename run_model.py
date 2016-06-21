import importlib
import copy
import queue

q=queue.Queue() #1

model_calc=importlib.import_module('calculator')  #2
calculator_object=getattr(model_calc,'calculator')() #5
input=getattr(calculator_object,'input')() #7

q.put(copy.deepcopy(calculator_object)) #10
q.put(copy.deepcopy(calculator_object)) #10

## Model Add

calculator_object = q.get() #11
add=getattr(calculator_object,'add')(extra=2) #7

q.put(copy.deepcopy(calculator_object)) #


## Model Sub
calculator_object = q.get()
sub=getattr(calculator_object,'subtract')()

q.put(copy.deepcopy(calculator_object))

## Model print
calculator_object = q.get()
res=getattr(calculator_object,'result')()
calculator_object = q.get()
res=getattr(calculator_object,'result')()
