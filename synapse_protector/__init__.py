# Copyright 2022 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, Dict

import attr
from synapse.module_api import ModuleApi, UserID
from synapse.module_api.errors import ConfigError

@attr.s(auto_attribs=True, frozen=True)
class ProtectorConfig:
    users: list[str]
    rooms: list[str]


class Protector:
    def __init__(self, config: ProtectorConfig, api: ModuleApi):
        # Keep a reference to the config and Module API
        self._config = config

        api.register_third_party_rules_callbacks(
            check_can_shutdown_room=self.check_can_shutdown_room,
            check_can_deactivate_user=self.check_can_deactivate_user,
        )

    async def check_can_shutdown_room(self, user_id: str, room_id: str):
        return not room_id in self._config.rooms

    async def check_can_deactivate_user(self, user_id: str, by_admin: bool):
        return not user_id in self._config.users

    @staticmethod
    def parse_config(config: Dict[str, Any]) -> ProtectorConfig:
        # Parse the module's configuration here.
        # If there is an issue with the configuration, raise a
        # synapse.module_api.errors.ConfigError.
        #
        # Example:
        #
        #     some_option = config.get("some_option")
        #     if some_option is None:
        #          raise ConfigError("Missing option 'some_option'")
        #      if not isinstance(some_option, str):
        #          raise ConfigError("Config option 'some_option' must be a string")
        #
        users = config.get("users", [])
        if not isinstance(users, list):
            raise ConfigError("Expected 'users' option to be a list")
    
        for user_id in users:
            if not UserID.is_valid(user_id):
                raise ConfigError(f"'users' option contained an invalid user id: {user_id}")

        rooms = config.get("rooms", [])
        if not isinstance(rooms, list):
            raise ConfigError("Expected 'rooms' option to be a list")

        for room_id in rooms:
            # No exposed way to check RoomID, so just do a simple sanity check.
            if not room_id.startswith('!'):
                raise ConfigError(f"'rooms' option contained an invalid room id: {room_id}")

        return ProtectorConfig(
            users=users,
            rooms=rooms
        )
