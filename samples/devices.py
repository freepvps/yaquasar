import asyncio
import aiohttp
import os
from yah import QuasarApi, SessionIdAuthorization


SESSION_ID = os.environ['YANDEX_SESSION_ID']


async def main():
    authorization=SessionIdAuthorization(SESSION_ID)
    async with QuasarApi(authorization=authorization) as api:
        res = await api.user.devices()
        for household in res.households:
            print(f'household: {household.name} ({household.id})')
            for room in household.rooms:
                print(f'- room: {room.name} ({room.id})')
                for device in room.devices:
                    print(f'  - device: {device.name} ({device.id})')
                    print(f'    capabilities:')
                    for capability in device.capabilities:
                        print(f'    - {capability.type}')
                    print(f'    properties:')
                    for property in device.properties:
                        print(f'    - {property.type}')


if __name__ == '__main__':
    asyncio.run(main())
