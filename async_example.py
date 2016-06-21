import asyncio
import time
import queue
import functools

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))
    return result

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(print_sum(1,2)),asyncio.ensure_future(print_sum(1,2))]
final=loop.run_until_complete(asyncio.gather(*tasks))
print(final)
loop.close()
