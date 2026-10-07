#!/usr/bin/env python3
"""Publish the released Inertance visitor files under a second domain."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
source = args.source.resolve()
output = args.output.resolve()
if output == source or source in output.parents or output.exists():
    parser.error("output must be a new directory outside the source tree")
revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
output.mkdir(parents=True)
for name in ("index.html", "app", "lab", "about", "assets", "robots.txt", "sitemap.xml", "LICENSE"):
    origin = source / name
    target = output / name
    if origin.is_dir():
        shutil.copytree(origin, target)
    else:
        shutil.copy2(origin, target)
for path in output.rglob("*"):
    if path.is_symlink():
        raise ValueError(f"Unexpected symlink: {path}")
    if path.is_file() and path.suffix in (".html", ".xml", ".txt", ".json", ".svg", ".css", ".js"):
        content = path.read_text()
        rewritten = content.replace("https://inertance.org", "https://hydraulicanalogy.com")
        if rewritten != content:
            path.write_text(rewritten)
(output / ".nojekyll").touch()
(output / "release.json").write_text(json.dumps({
    "upstream_repository": "Lucasfrit/inertance-site",
    "upstream_revision": revision,
    "site": "https://hydraulicanalogy.com/",
}, indent=2) + "\n")
for name in ("index.html", "app/index.html", "lab/index.html", "about/index.html"):
    content = (output / name).read_text()
    if "https://inertance.org" in content:
        raise ValueError(f"Primary-domain link remained in {name}")
print(f"Prepared hydraulicanalogy.com from inertance-site {revision}")
