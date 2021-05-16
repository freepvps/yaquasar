import typing
import dataclasses as dc
from .raw_client import RawClient


T = typing.TypeVar('T')


@dc.dataclass
class ApiStorage:
    _client: RawClient
    _apis: typing.Dict[typing.Type[typing.Any], typing.Any] = dc.field(default_factory=dict)

    def get_api(self, api_type: typing.Type[T]) -> T:
        if not issubclass(api_type, ApiBase):
            raise ValueError('Invalid api type')

        if api_type not in self._apis:
            self._apis[api_type] = api_type(client=self._client, storage=self)
        result: T = self._apis[api_type]
        return result


@dc.dataclass
class ApiBase:
    client: RawClient
    storage: ApiStorage
