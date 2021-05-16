import dataclasses as dc
from .._api_base import ApiBase
from ..types import HouseholdsResponse


@dc.dataclass
class UserApi(ApiBase):
    async def devices(self) -> HouseholdsResponse:
        return await self.client.get('v2/user/devices', HouseholdsResponse)
