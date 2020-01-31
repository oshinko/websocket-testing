import asyncio

import aiohttp

url = 'http://localhost:8000'


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                print(msg)


if __name__ == '__main__':
    asyncio.run(main())
