from typing import Optional, Type, TypeVar

from .providers import RandBankCard, RandEmail, RandFirstName, RandLastName, RandPhone, RandText, RandWord

Providers = TypeVar(
    "Providers",
    RandFirstName,
    RandLastName,
    RandEmail,
    RandWord,
    RandText,
    RandPhone,
    RandBankCard,
)


class RandGen:
    def __init__(self, provider: Type[Providers]) -> None:
        if not isinstance(
            provider,
            (type(RandFirstName), type(RandLastName), type(RandEmail), type(RandWord)),
        ):
            raise ValueError("Provider should only be a class" " (RandFirstName, RandLastName, RandEmail," " RandWord)")
        self.provider = provider()

    def generate(self, length: Optional[int] = None) -> str:
        return self.provider.generate(length=length)
