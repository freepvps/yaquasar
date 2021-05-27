import asyncio
import os
from yah import QuasarApi, XTokenAuthorization


X_TOKEN = os.environ['YANDEX_X_TOKEN']  # from Session_id cookie


async def main() -> None:
    authorization = XTokenAuthorization(X_TOKEN)
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
                        print(f'    - {capability.type} {capability.state} {capability.parameters}')
                    print(f'    properties:')
                    for property in device.properties:
                        print(f'    - {property.type} {property.state} {property.parameters}')


if __name__ == '__main__':
    asyncio.run(main())
