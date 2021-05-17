import dataclasses as dc
from .._api_base import RawClient, ApiStorage


@dc.dataclass
class AuthorizationBase:
    def initialize(self, client: RawClient, apis: ApiStorage) -> None:
        pass
