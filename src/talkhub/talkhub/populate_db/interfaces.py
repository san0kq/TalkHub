from typing import Protocol


class CreateRecordProtocol(Protocol):
    def create(self, data: object) -> None:
        raise NotImplementedError


class FakeFactoryProtocol(Protocol):
    def generate(self) -> object:
        raise NotImplementedError
