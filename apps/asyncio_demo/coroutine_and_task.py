#!/usr/bin/env python
# coding: utf-8

import asyncio
import time

"""
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


# async def main():
#     print(f"started at {time.strftime('%X')}")
#
#     await say_after(1, 'hello')
#     await say_after(2, 'world')
#
#     print(f"finished at {time.strftime('%X')}")

# asyncio.create_task() 函数用来并发运行作为 asyncio 任务 的多个协程
async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    # task2 = asyncio.create_task(say_after(2, 'world'))    # py3.7
    task2 = asyncio.ensure_future(say_after(2, 'ok'))   # py3.6
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
"""

# 可等待对象， 对象可以在await中使用， 主要类型：协程, 任务 和 Future.
# 协程
"""
async def nested():  # 协程函数
    return 42


async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    # nested()

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".   # await nested() 协程函数对应的对象


asyncio.run(main())
"""
# 任务 被用来设置日程以便 并发 执行协程
"""
import asyncio


async def nested_task():
    return 43


async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested_task())   # py3.7 before asyncio.ensure_future

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    print(await task)


asyncio.run(nested_task())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main)
"""
# Future 对象 是一种特殊的 低层级 可等待对象，表示一个异步操作的 最终结果
# 当一个 Future 对象 被等待，这意味着协程将保持等待直到该 Future 对象在其他地方操作完毕。
# 在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码。
# 返回对象的低层级函数的示例, 这个方法返回一个 asyncio.Future 对象
# https://docs.python.org/zh-cn/3.7/library/asyncio-future.html#asyncio.Future
import concurrent.futures


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()
    # loop = asyncio.get_event_loop()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool', result)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
asyncio.run(main(), debug=True)

# asyncio.gather 并发运行任务
"""
awaitable asyncio.gather(*aws, loop=None, return_exceptions=False)¶
并发 运行aws中的 可等待对象，如果aws中的某个可等待对象为协程，它将自动作为一个任务加入日程
如果所有可等待对象都成功完成，结果将是一个由所有返回值聚合而成的列表。结果值的顺序与 aws中可等待对象的顺序一致
如果 return_exceptions 为 False (默认)，所引发的首个异常会立即传播给等待 gather() 的任务。aws 序列中的其他可等待对象 不会被取消 并将继续运行。
如果 return_exceptions 为 True，异常会和成功的结果一样处理，并聚合至结果列表
如果 gather() 被取消，所有被提交 (尚未完成) 的可等待对象也会 被取消
"""
import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )


asyncio.run(main())
