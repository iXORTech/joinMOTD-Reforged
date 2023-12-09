from mcdreforged.api.all import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()


def i18n(translation_key: str, *args) -> str:
    return server.tr("joinmotd_reforged.{}".format(translation_key), *args)
