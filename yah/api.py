import typing
from .apis import UserApi, CsrfApi
from ._api_base import ApiHost
from ._base import DEFAULT_QUASAR_API_URL
from .auth import AuthorizationBase
from ._middlewares import CsrfMiddleware, HttpRetryMiddleware


class QuasarApi(ApiHost):
    def __init__(self, authorization: AuthorizationBase) -> None:
        super().__init__(url_base=DEFAULT_QUASAR_API_URL)
        self.client.session.middlewares.append(HttpRetryMiddleware())
        authorization.initialize(self.client, self.storage)
        self.client.session.middlewares.append(CsrfMiddleware(self.storage.get_api(CsrfApi)))

    async def __aenter__(self) -> 'QuasarApi':
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)

    @property
    def user(self) -> UserApi:
        return self.storage.get_api(UserApi)
