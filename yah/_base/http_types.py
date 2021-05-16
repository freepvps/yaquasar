import typing


# TODO: maybe 


QueryParams = typing.Dict[str, str]
Cookies = typing.Dict[str, str]
Headers = typing.Dict[str, str]


class RequestContext(typing.NamedTuple):
    query: QueryParams
    cookies: Cookies
    headers: Headers
