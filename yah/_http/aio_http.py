import typing
import dataclasses as dc
from aiohttp import ClientSession, ClientResponse
from .types import Request, Response, RequestMakerBase


@dc.dataclass
class AioHttpResponse(Response):
    base: ClientResponse

    @property
    def status(self) -> int:
        return self.base.status

    async def read(self) -> bytes:
        return await self.base.read()

    async def text(self) -> str:
        return await self.base.text()

    async def json(self) -> typing.Any:
        return await self.base.json()


@dc.dataclass
class AioHttpRequestMaker(RequestMakerBase):
    session: ClientSession = dc.field(default_factory=ClientSession)

    async def request(self, request: Request) -> Response:
        response: ClientResponse = await self.session.request(
            request.method.value,
            request.url,
            params=request.params or None,
            cookies=request.cookies or None,
            headers=request.headers or None,
            data=request.data,
            json=request.json,
        )
        return AioHttpResponse(response)

    async def __aenter__(self) -> 'RequestMakerBase':
        await self.session.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None:
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
