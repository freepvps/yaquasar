# yah
Yandex smart home apis

# Install
```sh
pip install git+https://github.com/sunsx0/yah
```

# Example
```python
import asyncio
import os
from yah import QuasarApi, SessionIdAuthorization


async def main():
    authorization=SessionIdAuthorization('3:1618855...')  # Session_id cookie
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
```
