from typing import List, Optional, Union

from mcdreforged.api.all import Serializable, ServerInterface

from joinmotd_reforged.server_info import ServerInfo

plugin_server_interface = ServerInterface.get_instance().as_plugin_server_interface()


class Config(Serializable):
    """
    The config class for JoinMOTD Reforged.
    """

    # The default config values.

    serverName: str = "Minecraft Server"
    currentServerName: str = "Survival Server"
    serverList: List[Union[str, ServerInfo]] = [
        ServerInfo(name="survival", description="Survival Server"),
        ServerInfo(name="creative", description="Creative Server"),
        ServerInfo(name="mirror", description="Mirror Server")
    ]

    start_day: Optional[str] = None
    daycount_plugin_ids: List[str] = [
        'mcd_daycount',
        'day_count_reforged',
        'daycount_nbt'
    ]
