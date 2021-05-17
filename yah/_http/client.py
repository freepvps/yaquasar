import typing
import dataclasses as dc
from .types import Request, Response, MiddlewareProxy, RequestMakerBase, RequestMiddlewareBase


@dc.dataclass(frozen=True)
class Client(RequestMakerBase):
    request_maker: RequestMakerBase
    middlewares: typing.List[RequestMiddlewareBase] = dc.field(default_factory=list)

    async def request(self, request: Request) -> Response:
        request_maker: RequestMakerBase = self.request_maker
        for middleware in reversed(self.middlewares):
            request_maker = MiddlewareProxy(
                middleware=middleware,
                next_maker=request_maker,
            )
        return await request_maker.request(request)

    async def __aenter__(self) -> 'Client':
        await self.request_maker.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None:
        await self.request_maker.__aexit__(exc_type, exc_val, exc_tb)
