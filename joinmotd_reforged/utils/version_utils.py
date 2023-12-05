import json
import re

from mcdreforged.api.all import PluginServerInterface, ServerInterface

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()


def load_version_properties():
    with server.open_bundled_file(f"version.json") as f:
        return json.load(f)


def get_version_property(value: str) -> str:
    return load_version_properties()[value]


def get_version() -> str:
    version_property = get_version_property("version")
    revision_property = get_version_property("revision")
    revision_property = revision_property.upper()
    stage_property = get_version_property("stage")
    if stage_property == "stable":
        version_property = f"{version_property} ({revision_property})"
        return version_property
    stage_property = re.sub(r"dev", "DEV", stage_property)
    stage_property = re.sub(r"alpha\.", "Alpha ", stage_property)
    stage_property = re.sub(r"alpha", "Alpha", stage_property)
    stage_property = re.sub(r"beta\.", "Beta ", stage_property)
    stage_property = re.sub(r"beta", "Beta", stage_property)
    stage_property = re.sub(r"rc\.", "Release Candidate ", stage_property)
    stage_property = re.sub(r"rc", "Release Candidate", stage_property)
    version_property = f"{version_property} {stage_property} ({revision_property})"
    return version_property


def get_build_date() -> str:
    return get_version_property("build_date")
