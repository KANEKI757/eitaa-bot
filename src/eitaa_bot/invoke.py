from __future__ import annotations

from typing import Any, Protocol


class Transport(Protocol):
    async def request(
        self,
        method: str,
        params: dict[str, Any],
        *,
        token: str | None = None,
    ) -> Any:
        ...


class RawInvoker:
    """
    Low-level access to Eitaa methods.

    This layer remains available even when
    generated/high-level wrappers exist.
    """

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def invoke(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        token: str | None = None,
    ) -> Any:
        return await self._transport.request(
            method,
            params or {},
            token=token,
        )
