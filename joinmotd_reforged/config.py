from typing import Dict, List, Optional, Union

from mcdreforged.api.all import Serializable, ServerInterface

from joinmotd_reforged.server_info import ServerInfo

plugin_server_interface = ServerInterface.get_instance().as_plugin_server_interface()


class Config(Serializable):
    """
    The config class for JoinMOTD Reforged.
    """

    # The default config values.

    server_name: str = "Minecraft Server"
    current_server_name: str = "Survival Server"
    server_list: List[Union[str, ServerInfo]] = [
        ServerInfo(name="survival", description="Survival Server"),
        ServerInfo(name="creative", description="Creative Server"),
        ServerInfo(name="mirror", description="Mirror Server")
    ]

    permission: Dict[str, int] = {
        'motd': 0,
        'server': 0,
        'reload': 3
    }

    start_day: Optional[str] = None
