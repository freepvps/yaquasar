import dataclasses as dc
from .devices import DevicesApi
from .._api_base import ApiBase


@dc.dataclass
class UserApi(ApiBase):
    @property
    def devices(self) -> DevicesApi:
        return self.storage.get_api(DevicesApi)
