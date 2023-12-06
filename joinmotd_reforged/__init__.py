import os
from datetime import datetime
from typing import Any, Callable, Union

from mcdreforged.api.all import *

from joinmotd_reforged.config import Config
from joinmotd_reforged.server_info import ServerInfo
from joinmotd_reforged.utils.version_utils import get_version, get_build_date

MOTD_PREFIX = '!!motd'
SERVER_LIST_PREFIX = '!!server'

config: Config
ConfigFilePath = os.path.join('config', 'joinMOTD-Reforged.json')


def load_config(server: PluginServerInterface):
    global config
    config = server.load_config_simple(file_name=ConfigFilePath, in_data_folder=False, target_class=Config)


def get_day(server: ServerInterface) -> str:
    try:
        startday = datetime.strptime(config.start_day, '%Y-%m-%d')
        now = datetime.now()
        output = now - startday
        return str(output.days)
    except Exception:
        pass

    daycount_plugin_id = "daycount_nbt"
    api = server.get_plugin_instance(daycount_plugin_id)
    if hasattr(api, 'getday') and callable(api.getday):
        return api.getday()

    try:
        import daycount
        return daycount.getday()
    except Exception:
        return '?'


def display_motd(server: ServerInterface, reply: Callable[[Union[str, RTextBase]], Any], player=None):
    """
    Display MOTD to the user
    """
    player = player if player else 'Console'
    reply('§7=======§r §6{}§r, welcome back to §9{}§r! §7=======§r'.format(player, config.current_server_name))
    reply('The server is running for §e{}§r days'.format(get_day(server)))
    display_server_list(reply)


def display_server_list(reply: Callable[[Union[str, RTextBase]], Any]):
    """
    Display Server List to the user
    """
    reply('§7-----------------§r Server List §7-----------------§r')

    messages = []
    for server in config.server_list:
        command = '/server {}'.format(server.name)
        hover_text = command
        if server.description is not None:
            hover_text = server.description + '\n' + command
        messages.append(RText('[{}]'.format(server.name)).h(hover_text).c(RAction.run_command, command))
    reply(RTextBase.join(' ', messages))


def register_commands(server: PluginServerInterface):
    """
    Register commands to the server
    """

    def get_literal_node(literal):
        lvl = config.permission.get(literal, 0)
        return Literal(literal).requires(
            lambda src: src.has_permission(lvl),
            lambda: "§cYou don't have permission to use this command!"
        )

    server.register_help_message(MOTD_PREFIX, '[joinMOTD-Reforged] Show Message of the Day')
    server.register_help_message(f"{MOTD_PREFIX} reload", '[joinMOTD-Reforged] Reload MOTD config')
    server.register_help_message(SERVER_LIST_PREFIX, '[joinMOTD-Reforged] Show Server List')

    server.register_command(
        get_literal_node(MOTD_PREFIX)
        .runs(lambda src: display_motd(src.get_server(), src.reply, src.player if src.is_player else None))
        .then(get_literal_node('reload').runs(load_config))
    )
    server.register_command(
        get_literal_node(SERVER_LIST_PREFIX).runs(lambda src: display_server_list(src.reply))
    )


def on_load(server: PluginServerInterface, old):
    load_config(server)
    register_commands(server)

    server.logger.info("==========================================================")
    server.logger.info("joinMOTD-Reforged is loaded!")
    plugin_version = get_version()
    plugin_build_date = get_build_date()
    server.logger.info(f"Version: {plugin_version} (Built on {plugin_build_date})")
    if "DEV" in plugin_version or "Alpha" in plugin_version or "Beta" in plugin_version:
        server.logger.info("§cTHIS IS IN EXPERIMENTAL STAGE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    elif "Release Candidate" in plugin_version:
        server.logger.info("§eTHIS IS A RELEASE CANDIDATE, PLEASE REPORT BUGS TO THE AUTHOR!")
    server.logger.info("==========================================================")


def on_player_joined(server: ServerInterface, player, info):
    display_motd(server, lambda msg: server.tell(player, msg))
