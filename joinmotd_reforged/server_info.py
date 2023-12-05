from typing import Optional

from mcdreforged.api.all import Serializable


class ServerInfo(Serializable):
    """
    Server Info structure to switch between servers.
    Credits to @Fallen_Breath (https://github.com/TISUnion/joinMOTD/)
    """

    name: str
    description: Optional[str] = None

    @classmethod
    def from_object(cls, obj) -> 'ServerInfo':
        if isinstance(obj, cls):
            return obj
        return ServerInfo(name=str(obj))
