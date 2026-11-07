#!/usr/bin/env python3
"""Copy the FLARE fire-model documentation into docs/flare/.

The pages are maintained in erf-model/FLARE (Docs/sphinx_doc). This script
reads them from a FLARE git checkout at a given ref, so edits belong in FLARE
and this copy is refreshed by rerunning the script:

    python3 tools/sync_flare_docs.py --flare /path/to/FLARE --ref origin/development

What it copies:

* ``Docs/sphinx_doc/theory/Fire.rst`` and every page in its toctree;
* the Fire Model section of ``Docs/sphinx_doc/Inputs.rst`` (from the
  ``sec:FireInputs`` label to the next ``sec:`` label) as ``inputs.rst``;
* every figure those pages use, into ``docs/flare/figures/``.

What it changes in the copy:

* a comment naming the source file and commit at the top of each page, and a
  note with the commit under the title of ``Fire.rst``;
* figure paths, to ``figures/<name>``;
* the inputs page title, to "Fire Model Inputs";
* a ``:ref:`` to a label that is neither in the copied pages nor in the ERF
  documentation (resolved by intersphinx, see docs/conf.py) becomes a link to
  the FLARE source page on GitHub. The ERF inventory is read from
  https://erf.readthedocs.io/en/latest/objects.inv.

``--check`` exits with status 1 when docs/flare/ differs from what the script
would write, without writing anything.
"""

import argparse
import filecmp
import io
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "flare"
DOCS = "Docs/sphinx_doc"
FLARE_URL = "https://github.com/erf-model/FLARE/blob/development"
ERF_INV = "https://erf.readthedocs.io/en/latest/objects.inv"

LABEL_RE = re.compile(r"^\.\. _([^\n]+):\s*$", re.M)
REF_RE = re.compile(r":ref:`([^`<]*?)(?:\s*<([^>`]+)>)?`")
FIG_RE = re.compile(r"^(\.\. (?:figure|image)::\s*)\.\./figures/(\S+)", re.M)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True).stdout


def show(repo, ref, path):
    return git(repo, "show", f"{ref}:{path}").decode()


def toctree_entries(text):
    """Page names listed in the toctree directives of a page."""
    names, inside = [], False
    for line in text.splitlines():
        if line.startswith(".. toctree::"):
            inside = True
            continue
        if inside:
            if line.strip() == "" or line.lstrip().startswith(":"):
                continue
            if line.startswith("   "):
                names.append(line.strip())
                continue
            inside = False
    return names


def erf_labels():
    """Lower-case std:label names in the ERF documentation inventory."""
    req = urllib.request.Request(ERF_INV, headers={"User-Agent": "sync_flare_docs"})
    with urllib.request.urlopen(req, timeout=60) as f:
        data = f.read()
    stream = io.BytesIO(data)
    for _ in range(4):  # four header lines
        stream.readline()
    body = zlib.decompress(stream.read()).decode()
    labels = set()
    for line in body.splitlines():
        parts = line.split(" ", 2)
        if len(parts) >= 2 and parts[1] == "std:label":
            labels.add(parts[0].lower())
    return labels


def flare_label_pages(repo, ref):
    """Label -> FLARE source path, for every page in FLARE's docs."""
    pages = git(repo, "ls-tree", "-r", "--name-only", ref, DOCS).decode().split()
    where = {}
    for path in pages:
        if not path.endswith(".rst"):
            continue
        for label in LABEL_RE.findall(show(repo, ref, path)):
            where.setdefault(label.strip().lower(), path)
    return where


def extract_inputs(text):
    start = text.index(".. _sec:FireInputs:")
    end = text.find("\n.. _sec:", start + 1)
    block = text[start:end if end > 0 else len(text)].rstrip() + "\n"
    if "\nFire Model\n==========" not in block:
        sys.exit("sync_flare_docs: the Fire Model heading moved in Inputs.rst; "
                 "update extract_inputs()")
    return block.replace("\nFire Model\n==========\n",
                         "\nFire Model Inputs\n=================\n", 1)


def build(repo, ref, dest):
    sha = git(repo, "rev-parse", "--short=9", ref).decode().strip()
    fire = show(repo, ref, f"{DOCS}/theory/Fire.rst")
    pages = {"Fire": (f"{DOCS}/theory/Fire.rst", fire)}
    for name in toctree_entries(fire):
        path = f"{DOCS}/theory/{name}.rst"
        pages[name] = (path, show(repo, ref, path))
    pages["inputs"] = (f"{DOCS}/Inputs.rst",
                       extract_inputs(show(repo, ref, f"{DOCS}/Inputs.rst")))

    local = set()
    for _, text in pages.values():
        local.update(l.strip().lower() for l in LABEL_RE.findall(text))
    erf = erf_labels()
    flare = flare_label_pages(repo, ref)

    def fix_ref(m):
        title, target = m.group(1).strip(), m.group(2)
        label = (target or title).strip()
        key = label.lower()
        if key in local or key in erf:
            return m.group(0)
        if key not in flare:
            sys.exit(f"sync_flare_docs: label '{label}' is defined nowhere")
        text = title if target else label
        return f"`{text} <{FLARE_URL}/{flare[key]}>`__"

    figures = set()
    for name, (path, text) in pages.items():
        figures.update(f for _, f in FIG_RE.findall(text))
        text = FIG_RE.sub(r"\1figures/\2", text)
        text = REF_RE.sub(fix_ref, text)
        head = (f".. Copied from erf-model/FLARE {path} at {sha} by\n"
                f".. tools/sync_flare_docs.py. Edit the page in FLARE, then rerun the script.\n\n")
        if name == "Fire":
            text = re.sub(r"(\nFire Model\n==========\n)",
                          r"\1\n.. note::\n\n   This section is copied from the "
                          f"`FLARE documentation <{FLARE_URL}/{DOCS}>`__ at commit\n"
                          f"   ``{sha}``. File paths such as ``FireEngine/`` and "
                          "``Exec/`` refer to the FLARE repository.\n",
                          text, count=1)
        (dest / f"{name}.rst").write_text(head + text)
    if figures:
        (dest / "figures").mkdir()
    for fig in sorted(figures):
        (dest / "figures" / fig).write_bytes(
            git(repo, "show", f"{ref}:{DOCS}/figures/{fig}"))
    return sha


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--flare", required=True, type=Path,
                    help="path to a git checkout of erf-model/FLARE")
    ap.add_argument("--ref", default="origin/development",
                    help="FLARE ref to copy from (default: origin/development)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if docs/flare/ is out of date; write nothing")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        sha = build(args.flare, args.ref, tmp)
        if args.check:
            ok = OUT.is_dir() and same_tree(tmp, OUT)
            print(f"docs/flare/ {'matches' if ok else 'differs from'} FLARE {sha}")
            sys.exit(0 if ok else 1)
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.copytree(tmp, OUT)
    print(f"docs/flare/ written from FLARE {sha}")


if __name__ == "__main__":
    main()
