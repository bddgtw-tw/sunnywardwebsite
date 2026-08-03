#!/usr/bin/env python3
"""Build, sanitize and publish the private source into the dedicated public repo."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REMOTE = "https://github.com/bddgtw-tw/sunnywardwebsite.git"


def run(*command: str, cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def remove_public_path(path: Path) -> None:
    def make_writable_and_retry(function, target, _error) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    if path.is_dir():
        shutil.rmtree(path, onerror=make_writable_and_retry)
    else:
        os.chmod(path, stat.S_IWRITE)
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("public_checkout", type=Path)
    parser.add_argument("--push", action="store_true", help="Push the verified public commit to GitHub.")
    args = parser.parse_args()
    public = args.public_checkout.resolve()
    if not (public / ".git").is_dir():
        raise RuntimeError("Public checkout must be an existing Git repository.")
    remote = run("git", "remote", "get-url", "origin", cwd=public)
    if remote.rstrip("/") != EXPECTED_REMOTE.rstrip("/"):
        raise RuntimeError(f"Unexpected public remote: {remote}")
    if run("git", "status", "--porcelain", cwd=public):
        raise RuntimeError("Public checkout has uncommitted changes.")

    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_public_site.py")], cwd=ROOT, check=True)
    with tempfile.TemporaryDirectory(prefix="sunnyward-public-") as temp:
        export = Path(temp) / "site"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "export_public_deployment.py"), str(export)], cwd=ROOT, check=True)
        for child in public.iterdir():
            if child.name == ".git":
                continue
            remove_public_path(child)
        for child in export.iterdir():
            target = public / child.name
            shutil.copytree(child, target, copy_function=shutil.copyfile) if child.is_dir() else shutil.copyfile(child, target)

    run("git", "add", "-A", cwd=public)
    if not run("git", "status", "--porcelain", cwd=public):
        print("Public deployment is already current.")
        return 0
    run("git", "commit", "-m", "deploy: publish verified Sunnyward update", cwd=public)
    if args.push:
        run("git", "push", "origin", "main", cwd=public)
        print("Verified public deployment pushed.")
    else:
        print("Verified public deployment committed locally; rerun with --push to publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
