import asyncio
import time
import queue
import functools
import collections

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))
    return result

def sequence(q):
    raise Exception('spam','eggs')
    for i in range(2):
        time.sleep(1)
        q.put(i)

async def producer(q):
    sequence(q)

async def consumer(q):
    print('ohh')
    #q.get(1)

async def run_producer(q):
    result = await producer(q)
    return result

async def run_consumer(q):
    result = await consumer(q)
    return result

q=queue.Queue()
loop = asyncio.get_event_loop()
#tasks = [asyncio.ensure_future(run_producer(q)),asyncio.ensure_future(run_consumer(q))]
tasks = [asyncio.ensure_future(producer(q)),asyncio.ensure_future(consumer(q))]
result_producer, result_consumer=loop.run_until_complete(asyncio.gather(*tasks,return_exceptions = True))
print(result_producer)
if (isinstance(result_producer,Exception)):
    print('yeh exception',result_producer)
loop.close()
