class EitaaError(Exception):
    """Base exception for eitaa-bot."""


class EitaaTransportError(EitaaError):
    """Network or transport failure."""


class EitaaRPCError(EitaaError):
    """Eitaa returned an RPC error."""

    def __init__(
        self,
        code: int,
        text: str,
        method: str | None = None,
    ) -> None:
        self.code = code
        self.text = text
        self.method = method

        message = f"Eitaa RPC error {code}: {text}"

        if method:
            message = f"{method}: {message}"

        super().__init__(message)


class EitaaSchemaError(EitaaError):
    """Invalid or incompatible schema."""


class EitaaAuthError(EitaaError):
    """Authentication/session error."""
