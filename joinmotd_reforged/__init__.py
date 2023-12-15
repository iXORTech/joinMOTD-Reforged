import os
from typing import Any, Callable, Union

from mcdreforged.api.all import *

from joinmotd_reforged.config import Config
from joinmotd_reforged.server_info import ServerInfo
from joinmotd_reforged.utils.i18n_utils import i18n
from joinmotd_reforged.utils.version_utils import get_version, get_build_date

DAYCOUNT_PLUGIN_ID = "daycount_nbt"

MOTD_PREFIX = '!!motd'
SERVER_LIST_PREFIX = '!!server'

config: Config
ConfigFilePath = os.path.join('config', 'joinmotd_reforged', 'config.json')


def load_config(server: PluginServerInterface):
    global config
    config = server.load_config_simple(file_name=ConfigFilePath, in_data_folder=False, target_class=Config)


def get_day(server: ServerInterface) -> str:
    api = server.get_plugin_instance(DAYCOUNT_PLUGIN_ID)
    if hasattr(api, 'getday') and callable(api.getday):
        return api.getday()
    return i18n('error_msg.unable_to_get_day_count')


def display_motd(server: ServerInterface, reply: Callable[[Union[str, RTextBase]], Any], player=None):
    """
    Display MOTD to the user
    """
    player = player if player else i18n('console')
    reply(i18n('motd.welcome', player, config.server_name))
    reply(i18n('motd.current_server', config.current_server_name))
    reply(i18n('motd.day_count', get_day(server)))
    display_server_list(reply)


def display_server_list(reply: Callable[[Union[str, RTextBase]], Any]):
    """
    Display Server List to the user
    """
    reply(i18n('server_list'))

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
            lambda: i18n('command.no_permission')
        )

    server.register_help_message(MOTD_PREFIX, i18n('command.help_msg.motd'))
    server.register_help_message(f"{MOTD_PREFIX} reload", i18n('command.help_msg.reload'))
    server.register_help_message(SERVER_LIST_PREFIX, i18n('command.help_msg.server'))

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
    server.logger.info(i18n('loaded'))
    plugin_version = get_version()
    plugin_build_date = get_build_date(i18n('locale'))
    server.logger.info(i18n('version', plugin_version, plugin_build_date))
    if "DEV" in plugin_version or "Alpha" in plugin_version or "Beta" in plugin_version:
        server.logger.info(i18n('experimental_warning'))
    elif "Release Candidate" in plugin_version:
        server.logger.info(i18n('release_candidate_warning'))
    server.logger.info("==========================================================")


def on_player_joined(server: ServerInterface, player, info):
    display_motd(server, lambda msg: server.tell(player, msg), player)
