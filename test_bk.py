import threading
class mythread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, **bwargs):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.f = kwargs['f']
        self.bwargs = bwargs
        print('bwargs')
        print(bwargs)
        return

    def run(self):
        self.f(*self.args,**self.kwargs)
        return

def hi(*args,**kwargs):
    print ('hi')

def arg(*args,**kwargs):
    print(args)
    print('kwargs')
    print(kwargs)
 
for i in range(5):
    t1=mythread(args=(i,),kwargs={'f':hi},test='hi',how='any')
    t2=mythread(args=(i,),kwargs={'f':arg})
    t1.start()
    t2.start()
