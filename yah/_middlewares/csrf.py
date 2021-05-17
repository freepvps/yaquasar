import typing
import dataclasses as dc
from .._http import RequestMiddlewareBase, RequestMakerBase, Request, Response, Method
from ..exceptions import ApiHttpErrorException
from ..apis import CsrfApi


@dc.dataclass
class CsrfMiddleware(RequestMiddlewareBase):
    api: CsrfApi

    target_http_error_code: int = 403
    csrf_token: typing.Optional[str] = None

    async def on_request(self, request: Request, maker: RequestMakerBase) -> Response:
        if request.method == Method.GET:
            return await maker.request(request)
    
        if not self.csrf_token:
            self.csrf_token = await self.api.get_csrf_token()

        request.headers['x-csrf-token'] = self.csrf_token
        resp: Response = await maker.request(request)
        
        if resp.status == self.target_http_error_code:
            self.csrf_token = None
            raise ApiHttpErrorException(resp.status)
        return resp
