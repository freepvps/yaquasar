import dataclasses as dc
from .._base import http_types


@dc.dataclass
class AuthorizationBase:
    def fill_authorization(self, context: http_types.RequestContext) -> None:
        raise NotImplementedError()


@dc.dataclass
class SessionIdAuthorization(AuthorizationBase):
    session_id: str

    def fill_authorization(self, context: http_types.RequestContext) -> None:
        context.cookies['Session_id'] = self.session_id
