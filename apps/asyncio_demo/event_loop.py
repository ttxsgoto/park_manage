#!/usr/bin/env python
# coding: utf-8
"""
Describe:
https://zhuanlan.zhihu.com/p/59621713
1.事件循环
管理所有的事件，在整个程序运行过程中不断循环执行并追踪事件发生的顺序将它们放在队列中，空闲时调用相应的事件处理者来处理这些事件

2.Future
Future对象表示尚未完成的计算，还未完成的结果

3.Task
是Future的子类，作用是在运行某个任务的同时可以并发的运行多个任务
loop.create_task()  当task为finished状态时，有个result()的方法
asyncio.ensure_future()


获取协程返回值
方式一：
loop = asyncio.get_event_loop()
task = loop.create_task(coro)
task.result()

方式二：回调函数
def my_callback(future):
    return future.result()

task = loop.create_task(coro)
task.add_done_callback(my_callback)
"""
import asyncio
import time

"""
多任务执行
通过asyncio.wait()可以控制多任务，
asyncio.wait()是一个协程，不会阻塞，立即返回，返回的是协程对象
传入的参数是future或协程构成的可迭代对象。最后将返回值传给run_until_complete()
加入事件循环

# 多任务中返回值
# - loop.create_task()
# - add_done_callback(fature)
"""


def done_callback(future):
    print('result: ', future.result())


async def coroutine_example(name, time):
    print('begin')
    await asyncio.sleep(time)
    print('done name:', name)
    return f'result: {name}'


def main_task_result():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    time_list = [2, 3, 5, 1, 4]
    """begin create_task"""
    # tasks = [loop.create_task(coroutine_example('begin' + str(i), i)) for i in range(5)]
    tasks = [loop.create_task(coroutine_example('begin' + str(i), i)) for i in time_list]
    print(len(tasks))
    wait_coro = asyncio.wait(tasks)
    loop.run_until_complete(wait_coro)
    for task in tasks:
        print(f'result---{task.result()}')
    """end create_task"""
    """begin done callback"""
    tasks = []
    for i in time_list:
        task = loop.create_task(coroutine_example('callback ' + str(i), i))
        task.add_done_callback(done_callback)
        tasks.append(task)
    wait_coro01 = asyncio.wait(tasks)
    loop.run_until_complete(wait_coro01)
    """end done callback"""

    loop.close()
    print('end time:', time.time() - start_time)
    # asyncio.run(wait_coro)


if __name__ == '__main__':
    main_task_result()
