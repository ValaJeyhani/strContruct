class StrConstructError(ValueError):
    """StrConstruct base exception. All other exceptions in StrConstruct inherit
    from this exceptions."""


class StrConstructParseError(StrConstructError):
    """Raised when parsing fails. All StrConstruct objects can potentially raise this exception."""


class StrConstructBuildError(StrConstructError):
    """Raised when building fails. All StrConstruct objects can potentially raise this exception."""


class StrStopFieldError(StrConstructError):
    """Raised only by StrStopIf and when its condition is met."""
