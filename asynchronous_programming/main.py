# Coroutines
# Event loop
import asyncio
import time

from asgiref.sync import sync_to_async


async def fetch_data():
    await asyncio.sleep(2)
    return "Data fetched"


async def fetch_data_v2():
    await sync_to_async(time.sleep, thread_sensitive=False)(2)
    return "Data fetched"


async def main():
    print(time.time())

    data = [fetch_data_v2() for _ in range(20)]

    await asyncio.gather(*data)

    print(time.time())
    print(len(data))


asyncio.run(main())
