from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import DataError, IntegrityError

if TYPE_CHECKING:
    from interfaces import CreateRecordProtocol, FakeFactoryProtocol


class PopulateTable:
    def __init__(
        self,
        records_number: int,
        dao: CreateRecordProtocol,
        fake_factory: FakeFactoryProtocol,
    ) -> None:
        self._records_number = records_number
        self._dao = dao
        self._fake_factory = fake_factory

    def execute(self) -> None:
        for _ in range(self._records_number):
            check = True
            while check:
                try:
                    new_record = self._fake_factory.generate()
                    self._dao.create(data=new_record)
                except IntegrityError:
                    continue
                except DataError:
                    continue
                check = False
