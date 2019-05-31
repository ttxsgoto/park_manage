# coding: utf-8

"""
并发的正确方式
    asyncio.create_task()   # 将协程封装程Task
    asyncio.ensure_future()
    asyncio.wait()
    asyncio.gather()
    loop = asyncio.get_event_loop()
    task = loop.create_task(b())
    task = loop.gather()
    wait = loop.wait()
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


async def main():
    result = await asyncio.gather(a(), b()) # 输入协程顺序和返回的结果相对应
    print(f'---{result}')
    return result


if __name__ == '__main__':
    asyncio.run(main())
