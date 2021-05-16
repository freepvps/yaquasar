import typing
import dataclasses as dc
from aiohttp import ClientSession, hdrs, ClientResponse
from urllib import parse as urlparse
from .auth import AuthorizationBase
from .._base import as_dict, from_dict, http_types, DEFAULT_QUASAR_API_URL


T = typing.TypeVar('T')


def _query_encode(value: typing.Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (str, int, float)):
        return str(value)
    else:
        raise ValueError(f'Unsupported value type {type(value)} {value}')


OptionalQueryParamsAny = typing.Optional[typing.Dict[str, typing.Any]]
OptionalRequestParser = typing.Optional[typing.Callable[[ClientResponse], typing.Awaitable[T]]]


@dc.dataclass
class RawClient:
    session: ClientSession
    authorization: AuthorizationBase
    url_base: str = DEFAULT_QUASAR_API_URL

    def makerequest_context(
        self,
        query: OptionalQueryParamsAny = None,
        cookies: typing.Optional[http_types.Cookies] = None,
        headers: typing.Optional[http_types.Headers] = None,
    ) -> http_types.RequestContext:
        query_final: typing.Dict[str, str] = {
            k: _query_encode(v)
            for k, v in (query or {}).items()
        }
        context = http_types.RequestContext(
            query=query_final,
            cookies=cookies or {},
            headers=headers or {},
        )
        self.authorization.fill_authorization(context)
        return context

    async def request(
        self,
        method: str,
        path: str,
        result_type: typing.Type[T],
        *,
        query: OptionalQueryParamsAny = None,
        data: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        joined: str = urlparse.urljoin(self.url_base, path)
        context = self.makerequest_context(query=query)
        data_dict: typing.Optional[typing.Any] = None
        if data is not None:
            data_dict = as_dict(data)

        response = await self.session.request(
            method,
            joined,
            params=context.query,
            cookies=context.cookies,
            headers=context.headers,
            data=data_dict,
        )
        if response_parser is None:
            json = await response.json()
            return from_dict(result_type, json)
        else:
            return await response_parser(response)

    async def get(
        self,
        path: str,
        result_type: typing.Type[T],
        *,
        query: OptionalQueryParamsAny = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            hdrs.METH_GET,
            path,
            result_type,
            query=query,
            response_parser=response_parser,
        )

    async def post(
        self,
        path: str,
        result_type: typing.Type[T],
        *,
        query: OptionalQueryParamsAny = None,
        data: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            hdrs.METH_POST,
            path,
            result_type,
            query=query,
            data=data,
            response_parser=response_parser,
        )

    async def delete(
        self,
        path: str,
        result_type: typing.Type[T],
        *,
        query: OptionalQueryParamsAny = None,
        data: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            hdrs.METH_DELETE,
            path,
            result_type,
            query=query,
            data=data,
            response_parser=response_parser,
        )

    async def patch(
        self,
        path: str,
        result_type: typing.Type[T],
        *,
        query: OptionalQueryParamsAny = None,
        data: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            hdrs.METH_PATCH,
            path,
            result_type,
            query=query,
            data=data,
            response_parser=response_parser,
        )
