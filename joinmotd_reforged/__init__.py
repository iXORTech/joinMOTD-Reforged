import os
from typing import Any, Callable, Union

from mcdreforged.api.all import *
from datetime import datetime

from joinmotd_reforged.config import Config
from joinmotd_reforged.utils.version_utils import get_version

MOTD_PREFIX = '!!motd'
SERVER_LIST_PREFIX = '!!server'

config: Config
ConfigFilePath = os.path.join('config', 'joinMOTD-Reforged.json')


def get_day(server: ServerInterface) -> str:
    try:
        startday = datetime.strptime(config.start_day, '%Y-%m-%d')
        now = datetime.now()
        output = now - startday
        return str(output.days)
    except Exception:
        pass

    for pid in config.daycount_plugin_ids:
        api = server.get_plugin_instance(pid)
        if hasattr(api, 'getday') and callable(api.getday):
            return api.getday()

    try:
        import daycount
        return daycount.getday()
    except Exception:
        return '?'


def display_motd(server: ServerInterface, reply: Callable[[Union[str, RTextBase]], Any]):
    """
    Display MOTD to the user
    """
    reply('§7=======§r Welcome back to §e{}§7 =======§r'.format(config.server_name))
    reply('The server is running for §e{}§r days'.format(get_day(server)))


def display_server_list(server: ServerInterface, reply: Callable[[Union[str, RTextBase]], Any]):
    """
    Display Server List to the user
    """
    pass


def register_commands(server: PluginServerInterface):
    """
    Register commands to the server
    """
    server.register_help_message(MOTD_PREFIX, '[joinMOTD-Reforged] Show Message of the Day')
    server.register_help_message(SERVER_LIST_PREFIX, '[joinMOTD-Reforged] Show Server List')
    server.register_command(
        Literal(MOTD_PREFIX).runs(lambda src: display_motd(src.get_server(), src.reply))
    )
    server.register_command(
        Literal(SERVER_LIST_PREFIX).runs(lambda src: display_server_list(src.get_server(), src.reply))
    )


def on_load(server: PluginServerInterface, old):
    global config
    config = server.load_config_simple(file_name=ConfigFilePath, in_data_folder=False, target_class=Config)

    register_commands(server)

    server.logger.info("==========================================================")
    server.logger.info("joinMOTD-Reforged is loaded!")
    plugin_version = get_version()
    server.logger.info(f"Version: {plugin_version}")
    if "DEV" in plugin_version or "Alpha" in plugin_version or "Beta" in plugin_version:
        server.logger.info("§cTHIS IS IN EXPERIMENTAL STAGE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    elif "Release Candidate" in plugin_version:
        server.logger.info("§eTHIS IS A RELEASE CANDIDATE, PLEASE REPORT BUGS TO THE AUTHOR!")
    server.logger.info("==========================================================")
