from typing import Any


def standard_response(data: Any = None, message: str | None = None, meta: dict | None = None):
    payload = {"success": True, "data": data}
    if message:
        payload["message"] = message
    if meta:
        payload["meta"] = meta
    return payload
