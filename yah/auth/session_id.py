import typing
import dataclasses as dc
from .common import AuthorizationBase
from .._api_base import RawClient, ApiStorage
from .._http import Request, Response, RequestMakerBase, RequestMiddlewareBase


@dc.dataclass
class SessionIdAuthorization(AuthorizationBase, RequestMiddlewareBase):
    session_id: str
    yandex_uid: typing.Optional[str] = None

    def initialize(self, client: RawClient, apis: ApiStorage) -> None:
        client.session.middlewares.append(self)

    async def on_request(self, request: Request, maker: RequestMakerBase) -> Response:
        request.cookies['Session_id'] = self.session_id
        if self.yandex_uid:
            request.cookies['yandexuid'] = self.yandex_uid
        return await maker.request(request)
