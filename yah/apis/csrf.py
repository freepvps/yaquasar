import re
import typing
import dataclasses as dc
from .._api_base import ApiBase, forward_resp
from .._http.types import Response
from ..exceptions import ApiErrorException


RE_CSRF = re.compile('"csrfToken2":"(.+?)"')


@dc.dataclass
class CsrfApi(ApiBase):
    async def get_csrf_token(self) -> str:
        resp = await self.client.get(
            'https://yandex.ru/quasar/iot',
            Response,
            response_parser=forward_resp,
        )
        text = await resp.text()
        tokens = RE_CSRF.search(text)

        if not tokens:
            raise ApiErrorException('csrf token not found')
        
        return tokens[1]
