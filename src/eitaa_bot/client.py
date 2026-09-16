from __future__ import annotations

from typing import Any

import httpx

from .errors import EitaaRPCError, EitaaTransportError
from .invoke import RawInvoker


class EitaaTransport:
    def __init__(
        self,
        endpoint: str,
        *,
        timeout: float = 30.0,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.client = httpx.AsyncClient(
            http2=True,
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        params: dict[str, Any],
        *,
        token: str | None = None,
    ) -> Any:
        payload = {
            "method": method,
            "params": params,
        }

        headers: dict[str, str] = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = await self.client.post(
                self.endpoint,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise EitaaTransportError(str(exc)) from exc

        data = response.json()

        if isinstance(data, dict) and "error" in data:
            error = data["error"]

            if isinstance(error, dict):
                raise EitaaRPCError(
                    int(error.get("code", 0)),
                    str(
                        error.get(
                            "message",
                            error.get("text", "Unknown error"),
                        )
                    ),
                    method,
                )

        return data

    async def close(self) -> None:
        await self.client.aclose()


class EitaaClient:
    def __init__(
        self,
        endpoint: str,
        *,
        token: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.transport = EitaaTransport(
            endpoint,
            timeout=timeout,
        )

        self.token = token
        self.raw = RawInvoker(self.transport)

    async def invoke(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self.raw.invoke(
            method,
            params,
            token=self.token,
        )

    async def close(self) -> None:
        await self.transport.close()

    async def __aenter__(self) -> "EitaaClient":
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        await self.close()
