import typing
import dataclasses as dc
from .._api_base import ApiBase, forward_resp
from .._http.types import Response


@dc.dataclass
class XTokenAuthApi(ApiBase):
    async def login_token(self, x_token: str) -> bool:
        payload = {
            'type': 'x-token',
            'retpath': 'https://www.yandex.ru/androids.txt'
        }
        headers = {
            'Ya-Consumer-Authorization': f'OAuth {x_token}',
        }
        resp1: typing.Any = await self.client.post(
            'https://mobileproxy.passport.yandex.net/1/bundle/auth/x_token/',
            typing.Any,
            data=payload,
            headers=headers,
        )
        if resp1['status'] != 'ok':
            return False

        host: str = resp1['passport_host']
        payload = {'track_id': resp1['track_id']}

        resp2: Response = await self.client.get(
            f'{host}/auth/session/',
            Response,
            query=payload,
            response_parser=forward_resp,
        )
        if resp2.status != 404:
            raise ValueError(f'Status check failed {resp2.status}')

        return True

    async def check_cookie_is_valid(self) -> bool:
        resp: Response = await self.client.get(
            'https://quasar.yandex.ru/get_account_config',
            Response,
            response_parser=forward_resp,
        )
        data = await resp.json()
        return bool(data['status'] == 'ok')

    async def refresh_cookies(self, x_token: str) -> bool:
        return (
            await self.check_cookie_is_valid()
            or await self.login_token(x_token)
        )