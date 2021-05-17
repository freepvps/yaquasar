import argparse
import asyncio
import os
from yah import QuasarApi, XTokenAuthorization
from yah.types import on_off


X_TOKEN = os.environ['YANDEX_X_TOKEN']  # from Session_id cookie


async def main(args: argparse.Namespace) -> None:
    authorization = XTokenAuthorization(X_TOKEN)
    async with QuasarApi(authorization=authorization) as api:
        await api.user.devices.actions(
            args.device_id,
            [
                on_off.Capability(
                    state=on_off.State(value=args.enable == 'on'),
                ),
            ],
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('device_id')
    parser.add_argument('enable', choices=('on', 'off'))
    return parser.parse_args()



if __name__ == '__main__':
    asyncio.run(main(parse_args()))
