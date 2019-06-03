#!/usr/bin/env python
# coding: utf-8
"""
__author__ = zhongqiang

Created on  19/6/2

Describe:
    - create task
    - shield
    - asyncio.create_task(coro) ——> return task object
    - loop.create_task(coro)
    - asyncio.ensure_future(coro or future or awaitable object)
        - core , return task object
        - future , return
        - awaitable, again exec ensure_future, return task or future
"""
import asyncio


async def a():
    print('a')
    await asyncio.sleep(3)
    print('end a')
    return 'a'


async def b():
    print('b')
    await asyncio.sleep(1)
    print('end b')
    return 'b'


if __name__ == '__main__':
    asyncio.run()