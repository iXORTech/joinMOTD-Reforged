from mcdreforged.api.all import *


def on_load(server: PluginServerInterface, old):
    server.logger.info('Hello world!')
