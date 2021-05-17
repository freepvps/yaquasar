import typing
import dataclasses as dc
from urllib import parse as urlparse
from .._base import as_dict, from_dict, DEFAULT_QUASAR_API_URL
from .._http import Client, Method, Request, Response
from ..exceptions import ApiHttpErrorException


T = typing.TypeVar('T')


def _query_encode(value: typing.Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (str, int, float)):
        return str(value)
    else:
        raise ValueError(f'Unsupported value type {type(value)} {value}')


OptionalQueryParamsAny = typing.Optional[typing.Dict[str, typing.Any]]
OptionalHeaders = typing.Optional[typing.Mapping[str, str]]
OptionalCookies = typing.Optional[typing.Mapping[str, str]]
OptionalRequestParser = typing.Optional[typing.Callable[[Response], typing.Awaitable[T]]]
ResultType = typing.Union[typing.Type[T], typing.Any]


async def forward_resp(resp: Response) -> Response:
    return resp


@dc.dataclass
class RawClient:
    session: Client
    url_base: str = DEFAULT_QUASAR_API_URL

    async def request(
        self,
        method: Method,
        path: str,
        result_type: ResultType[T],
        *,
        query: OptionalQueryParamsAny = None,
        headers: OptionalHeaders = None,
        cookies: OptionalCookies = None,
        data: typing.Any = None,
        json: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        query_final: typing.Dict[str, str] = {
            k: _query_encode(v)
            for k, v in (query or {}).items()
        }
        data_dict: typing.Optional[typing.Any] = None
        json_dict: typing.Optional[typing.Any] = None
        if data is not None:
            data_dict = as_dict(data)
        if json is not None:
            json_dict = as_dict(json)

        request = Request(
            method=method,
            url=urlparse.urljoin(self.url_base, path),
            params=query_final,
            cookies=dict(cookies or {}),
            headers=dict(headers or {}),
            data=data_dict,
            json=json_dict,
        )

        response = await self.session.request(request)
        if response_parser is None:
            if response.status < 200 or response.status >= 300:
                raise ApiHttpErrorException(response.status)

            json = await response.json()
            result: T = from_dict(result_type, json)
            return result
        else:
            return await response_parser(response)

    async def get(
        self,
        path: str,
        result_type: ResultType[T],
        *,
        query: OptionalQueryParamsAny = None,
        headers: OptionalHeaders = None,
        cookies: OptionalCookies = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            Method.GET,
            path,
            result_type,
            query=query,
            headers=headers,
            cookies=cookies,
            response_parser=response_parser,
        )

    async def post(
        self,
        path: str,
        result_type: ResultType[T],
        *,
        query: OptionalQueryParamsAny = None,
        headers: OptionalHeaders = None,
        cookies: OptionalCookies = None,
        data: typing.Any = None,
        json: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            Method.POST,
            path,
            result_type,
            query=query,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json,
            response_parser=response_parser,
        )

    async def delete(
        self,
        path: str,
        result_type: ResultType[T],
        *,
        query: OptionalQueryParamsAny = None,
        headers: OptionalHeaders = None,
        cookies: OptionalCookies = None,
        data: typing.Any = None,
        json: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            Method.DELETE,
            path,
            result_type,
            query=query,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json,
            response_parser=response_parser,
        )

    async def patch(
        self,
        path: str,
        result_type: ResultType[T],
        *,
        query: OptionalQueryParamsAny = None,
        headers: OptionalHeaders = None,
        cookies: OptionalCookies = None,
        data: typing.Any = None,
        json: typing.Any = None,

        response_parser: OptionalRequestParser[T] = None,
    ) -> T:
        return await self.request(
            Method.PATCH,
            path,
            result_type,
            query=query,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json,
            response_parser=response_parser,
        )
