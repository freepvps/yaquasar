from .aio_http import AioHttpRequestMaker
from .client import Client


def create_client() -> Client:
    return Client(AioHttpRequestMaker())
