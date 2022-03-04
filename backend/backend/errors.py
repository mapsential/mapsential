class AdminBackendError(Exception):
    pass


_BaseError = AdminBackendError


class DatabaseError(_BaseError):
    pass


class DatabaseCrudError(DatabaseError):
    """Errors relating to create, read, update and delete database operations."""

    pass
