# coding: utf-8
"""
- eventloop
- coroutine
- Future
- Task future sub class

"""

import asyncio


async def a():
    print('a')
    await asyncio.sleep(0)
    print('end a')


async def b():
    print('b')


async def main():
    await asyncio.gather(*[a(), b()])


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

