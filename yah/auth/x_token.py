import dataclasses as dc
from .common import AuthorizationBase
from .._api_base import RawClient, ApiStorage
from ..apis import XTokenAuthApi
from .._middlewares import XTokenMiddleware


@dc.dataclass
class XTokenAuthorization(AuthorizationBase):
    x_token: str

    def initialize(self, client: RawClient, apis: ApiStorage) -> None:
        api = apis.get_api(XTokenAuthApi)
        client.session.middlewares.append(XTokenMiddleware(
            api,
            self.x_token
        ))
