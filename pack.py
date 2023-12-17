import os
import json
from datetime import datetime

version = "1.0.0"
stage = "stable"
revision: str
with os.popen("git rev-parse --short=7 HEAD") as f:
    revision = f.readline().strip()

build_date_en_us = datetime.today().strftime("%a., %B %d %Y")
build_date_zh_cn = datetime.today().strftime("%Y年%m月%d日")

version_properties = {
    "version": version,
    "stage": stage,
    "revision": revision,
    "build_date": {
        "en_us": build_date_en_us,
        "zh_cn": build_date_zh_cn
    }
}

version_properties_obj = json.dumps(version_properties)
version_properties_file = "version.json"

with open(version_properties_file, "w") as f:
    f.write(version_properties_obj)
    f.close()

project_dir = os.getcwd()

pack_version_string: str
if stage.startswith("dev") or stage.startswith("alpha") or stage.startswith("beta") or stage.startswith("rc"):
    pack_version_string = f"v{version}-{stage}+{revision}"
else:
    pack_version_string = f"v{version}+{revision}"

os.chdir(f"{project_dir}")
os.system(f"mcdreforged pack --output build/distributions "
          f"--name joinMOTD-Reforged-{pack_version_string}.mcdr --ignore-file .mcdrignore")
    