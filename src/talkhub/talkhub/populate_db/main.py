from .dao import UserDAO
from .factories import UserFactory
from .populate_table_command import PopulateTable
from .rand_gen import RandEmail, RandFirstName, RandGen, RandLastName, RandText, RandWord


def run():
    records_number = 10

    user_dao = UserDAO()
    user_factory = UserFactory(
        username_provider=RandGen(RandWord),
        email_profiver=RandGen(RandEmail),
        password_provider=RandGen(RandWord),
        first_name_provider=RandGen(RandFirstName),
        last_name_profivder=RandGen(RandLastName),
        about_provider=RandGen(RandText),
    )
    PopulateTable(records_number=records_number, dao=user_dao, fake_factory=user_factory).execute()
