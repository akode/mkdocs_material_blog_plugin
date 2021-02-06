import os.path

import pytest
from mkdocs import config
from mkdocs.commands import build


def test_plugin(tmpdir):
    mkdocs_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

    cfg = config.load_config(os.path.join(mkdocs_root, "mkdocs.yml"))
    cfg["site_dir"] = tmpdir
    build.build(cfg)
