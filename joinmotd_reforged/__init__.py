import os

from mcdreforged.api.all import *

from joinmotd_reforged.config import Config

Prefix = '!!joinMOTD'
config: Config
ConfigFilePath = os.path.join('config', 'joinMOTD-Reforged.json')


def on_load(server: PluginServerInterface, old):
    server.logger.info('Hello world!')
