class BackendError(Exception):
    pass


_BaseError = BackendError


class CountryCodeError(_BaseError):
    pass


class InternationalizedTermError(_BaseError):
    pass


class CustomColorModelError(_BaseError):
    pass


class DataManagementError(_BaseError):
    pass


class GeolocationError(DataManagementError):
    pass
