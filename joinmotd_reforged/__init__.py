import os

from mcdreforged.api.all import *

from joinmotd_reforged.config import Config
from joinmotd_reforged.utils.version_utils import get_version

Prefix = '!!joinMOTD'
config: Config
ConfigFilePath = os.path.join('config', 'joinMOTD-Reforged.json')


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
