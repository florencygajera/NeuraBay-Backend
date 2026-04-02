from typing import Any


async def chatbot_reply(message: str) -> dict[str, Any]:
    return {
        "reply": "NeuraBay AI module is in development.",
        "input": message,
    }
