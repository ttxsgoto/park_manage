# coding: utf-8
"""
同步代码异步执行

"""

import asyncio
from time import sleep
from concurrent.futures import ProcessPoolExecutor


async def sleep_async(loop, delay):
    # Can set executor to None if a default has been set for loop
    await loop.run_in_executor(ProcessPoolExecutor(), sleep, delay)
    print('---------')
    return 'I slept asynchronously'


loop = asyncio.get_event_loop()

loop.run_until_complete(sleep_async(loop, 2))


async def a():
    await asyncio.sleep(1)
    return 'ok'

asyncio.create_task(a())

