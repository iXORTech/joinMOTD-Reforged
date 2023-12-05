import os
from typing import Any, Callable, Union

from mcdreforged.api.all import *
from datetime import datetime

from joinmotd_reforged.config import Config
from joinmotd_reforged.utils.version_utils import get_version

COMMAND_PREFIX = '!!joinMOTD'
config: Config
ConfigFilePath = os.path.join('config', 'joinMOTD-Reforged.json')


def get_day(server: ServerInterface) -> str:
    try:
        startday = datetime.strptime(config.start_day, '%Y-%m-%d')
        now = datetime.now()
        output = now - startday
        return str(output.days)
    except:
        pass

    for pid in config.daycount_plugin_ids:
        api = server.get_plugin_instance(pid)
        if hasattr(api, 'getday') and callable(api.getday):
            return api.getday()

    try:
        import daycount
        return daycount.getday()
    except:
        return '?'


def display_motd(server: ServerInterface, reply: Callable[[Union[str, RTextBase]], Any]):
    """
    Display MOTD to the user
    """
    pass


def on_load(server: PluginServerInterface, old):
    global config
    config = server.load_config_simple(file_name=ConfigFilePath, in_data_folder=False, target_class=Config)

    server.logger.info("==========================================================")
    server.logger.info("joinMOTD-Reforged is loaded!")
    plugin_version = get_version()
    server.logger.info(f"Version: {plugin_version}")
    if "DEV" in plugin_version or "Alpha" in plugin_version or "Beta" in plugin_version:
        server.logger.info("§cTHIS IS IN EXPERIMENTAL STAGE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    elif "Release Candidate" in plugin_version:
        server.logger.info("§eTHIS IS A RELEASE CANDIDATE, PLEASE REPORT BUGS TO THE AUTHOR!")
    server.logger.info("==========================================================")

    server.register_help_message(COMMAND_PREFIX, "Show Help Message of joinMOTD-Reforged")
    server.register_command(
        Literal(COMMAND_PREFIX).runs(lambda src: display_motd(src.get_server(), src.reply))
    )
