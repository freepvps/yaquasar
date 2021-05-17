import typing
from .._http import create_client
from .raw_client import RawClient
from .api_storage import ApiStorage


class ApiHost:
    client: RawClient
    storage: ApiStorage

    def __init__(
        self,
        url_base: str,
    ) -> None:
        self.client = RawClient(
            session=create_client(),
            url_base=url_base,
        )
        self.storage = ApiStorage(self.client)

    async def __aenter__(self) -> 'ApiHost':
        await self.client.session.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None:
        await self.client.session.__aexit__(exc_type, exc_val, exc_tb)
