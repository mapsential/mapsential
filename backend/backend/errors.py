class BackendError(Exception):
    pass


_BaseError = BackendError


class CountryCodeError(BackendError):
    pass

class DataManagementError(BackendError):
    pass


class GeolocationError(DataManagementError):
    pass
