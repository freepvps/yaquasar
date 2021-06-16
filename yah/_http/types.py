import enum
import typing
import dataclasses as dc
from typing_extensions import Protocol


QueryParams = typing.Dict[str, str]
Cookies = typing.Dict[str, str]
Headers = typing.Dict[str, str]


class Method(enum.Enum):
    CONNECT = "CONNECT"
    HEAD = "HEAD"
    GET = "GET"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


@dc.dataclass
class Request:
    method: Method
    url: str
    params: QueryParams = dc.field(default_factory=dict)
    cookies: Cookies = dc.field(default_factory=dict)
    headers: Headers = dc.field(default_factory=dict)
    data: typing.Any = None
    json: typing.Any = None


class Response(Protocol):
    @property
    def status(self) -> int: ...
    async def read(self) -> bytes: ...
    async def text(self) -> str: ...
    async def json(self) -> typing.Any: ...


class RequestMakerBase(Protocol):
    async def request(self, request: Request) -> Response: ...
    async def __aenter__(self) -> 'RequestMakerBase': ...
    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None: ...


class RequestMiddlewareBase(Protocol):
    async def on_request(self, request: Request, maker: RequestMakerBase) -> Response: ...


@dc.dataclass(frozen=True)
class MiddlewareProxy(RequestMakerBase):
    middleware: RequestMiddlewareBase
    next_maker: RequestMakerBase

    async def request(self, request: Request) -> Response:
        return await self.middleware.on_request(request, self.next_maker)
