import typing
import dataclasses as dc
from .._api_base import ApiBase
from ..types import HouseholdsResponse, ResponseBase, CapabilityBase


@dc.dataclass
class ActionsRequest:
    actions: typing.Iterable[CapabilityBase]


@dc.dataclass
class DevicesApi(ApiBase):
    async def __call__(self) -> HouseholdsResponse:
        return await self.client.get('v2/user/devices', HouseholdsResponse)

    async def actions(self, device_id: str, actions: typing.Iterable[CapabilityBase]) -> ResponseBase:
        return await self.client.post(
            f'user/devices/{device_id}/actions',
            result_type=ResponseBase,
            json=ActionsRequest(actions),
        )
