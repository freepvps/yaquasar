import dataclasses as dc
from .._http import RequestMiddlewareBase, RequestMakerBase, Request, Response, Method
from ..exceptions import ApiHttpErrorException
from ..apis import XTokenAuthApi


@dc.dataclass
class XTokenMiddleware(RequestMiddlewareBase):
    api: XTokenAuthApi
    x_token: str

    target_http_error_code: int = 401

    async def on_request(self, request: Request, maker: RequestMakerBase) -> Response:
        resp: Response = await maker.request(request)
        if resp.status == self.target_http_error_code:
            await self.api.refresh_cookies(self.x_token)
            raise ApiHttpErrorException(resp.status)
        return resp
