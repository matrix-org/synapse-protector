import aiounittest

from synapse_protector import Protector
from . import create_module

class ExampleTest(aiounittest.AsyncTestCase):
    protector: Protector = create_module([
        "@deny:example"
    ], [
        "!deny:example"
    ])

    async def test_deny_protected_room(self) -> None:
        self.assertFalse(await self.protector.check_can_shutdown_room("@alice:example", "!deny:example"))

    async def test_deny_protected_user(self) -> None:
        self.assertFalse(await self.protector.check_can_deactivate_user("@deny:example", False))
        self.assertFalse(await self.protector.check_can_deactivate_user("@deny:example", True))

    async def test_allow_unrotected_room(self) -> None:
        self.assertTrue(await self.protector.check_can_shutdown_room("@alice:example", "!allow:example"))

    async def test_allow_unprotected_user(self) -> None:
        self.assertTrue(await self.protector.check_can_deactivate_user("@allow:example", False))
        self.assertTrue(await self.protector.check_can_deactivate_user("@allow:example", True))
