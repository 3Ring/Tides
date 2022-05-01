import asyncio
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> Any:
    """Runs given functions in sequence for asyncio"""
    for function in functions:
        rets = await function
    return rets


async def run_parallel(*functions: Awaitable[Any]) -> Any:
    """Runs given functions in parallel for asyncio"""
    return await asyncio.gather(*functions)
