import typing


class YahException(BaseException):
    pass


class ApiErrorException(YahException):
    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        self.message = message


class ApiHttpErrorException(ApiErrorException):
    http_code: int

    def __init__(self, http_code: int, *args: typing.Any) -> None:
        super().__init__(f'Unexpected http code {http_code}', *args)
        self.http_code = http_code
