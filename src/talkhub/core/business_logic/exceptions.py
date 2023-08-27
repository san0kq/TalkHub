class ConfirmationCodeNotExists(Exception):
    pass


class ConfirmationCodeExpired(Exception):
    pass


class InvalidAuthCredentials(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


class TagsError(Exception):
    pass


class PageDoesNotExists(Exception):
    pass
