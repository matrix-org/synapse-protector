from asyncio import Future
from typing import Any, Awaitable, Dict, Optional, TypeVar

import attr
from unittest.mock import Mock
from synapse.module_api import ModuleApi

from synapse_protector import Protector

TV = TypeVar("TV")


def make_awaitable(result: TV) -> Awaitable[TV]:
    """
    Makes an awaitable, suitable for mocking an `async` function.
    This uses Futures as they can be awaited multiple times so can be returned
    to multiple callers.
    This function has been copied directly from Synapse's tests code.
    """
    future = Future()  # type: ignore
    future.set_result(result)
    return future

def create_module(users: list[str], rooms: list[str]) -> Protector:
    # Create a mock based on the ModuleApi spec, but override some mocked functions
    # because some capabilities are needed for running the tests.
    module_api = Mock(spec=ModuleApi)

    # If necessary, give parse_config some configuration to parse.
    config = Protector.parse_config({
        "users": users,
        "rooms": rooms,
    })

    return Protector(config, module_api)
