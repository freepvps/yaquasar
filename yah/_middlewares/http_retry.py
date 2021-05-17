import dataclasses as dc
from .._http import RequestMiddlewareBase, RequestMakerBase, Request, Response
from ..exceptions import ApiHttpErrorException


# TODO: fix potential recursion
@dc.dataclass(frozen=True)
class HttpRetryMiddleware(RequestMiddlewareBase):
    max_retries: int = 3

    async def on_request(self, request: Request, maker: RequestMakerBase) -> Response:
        for _ in range(self.max_retries - 1):
            try:
                resp: Response = await maker.request(request)
                return resp
            except ApiHttpErrorException:
                continue
        return await maker.request(request)
