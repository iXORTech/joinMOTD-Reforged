import os
import json
from datetime import datetime

version = "0.0.1"
stage = "dev"
revision = "0000000"
with os.popen("git rev-parse --short=7 HEAD") as f:
    revision = f.readline().strip()

build_date = datetime.today().strftime("%a., %B %d %Y")

version_properties = {
    "version": version,
    "stage": stage,
    "revision": revision,
    "build_date": build_date
}

version_properties_obj = json.dumps(version_properties)
version_properties_file = "joinmotd_reforged/version.json"

with open(version_properties_file, "w") as f:
    f.write(version_properties_obj)
    f.close()

project_dir = os.getcwd()

os.chdir(f"{project_dir}")
os.system("mcdreforged pack -o build/distributions")

os.chdir(f"{project_dir}/build/distributions")
if stage == "dev" or stage == "alpha" or stage == "beta" or stage == "rc":
    os.rename(
        f"JoinMOTDReforged-v{version}-{stage}.mcdr",
        f"joinMOTD-Reforged-v{version}-{stage}+{revision}.mcdr"
    )
else:
    os.rename(
        f"JoinMOTDReforged-v{version}.mcdr",
        f"joinMOTD-Reforged-v{version}+{revision}.mcdr"
    )
    